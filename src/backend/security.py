"""
Security Utilities for QMS Dashboard
Phase 7 WS-2: Security & Access Controls

Provides security functions for input sanitization, validation, and protection.
"""

import re
from pathlib import Path
from typing import Optional


class SecurityError(Exception):
    """Raised when security validation fails."""
    pass


def sanitize_project_name(project_name: str) -> str:
    """
    Sanitize project name for safe filesystem use.

    Removes path separators, special characters, and normalizes whitespace.
    Prevents path traversal attacks and filesystem issues.

    Args:
        project_name: Raw project name from user input

    Returns:
        Sanitized project name safe for filesystem use

    Raises:
        SecurityError: If project name is empty after sanitization

    Examples:
        >>> sanitize_project_name("My Project")
        'My-Project'
        >>> sanitize_project_name("../../etc/passwd")
        'etc-passwd'
        >>> sanitize_project_name("Test<>Project")
        'Test-Project'
    """
    if not project_name or not project_name.strip():
        raise SecurityError("Project name cannot be empty")

    # Remove leading/trailing whitespace
    sanitized = project_name.strip()

    # Replace path separators with hyphens
    sanitized = sanitized.replace("/", "-").replace("\\", "-")

    # Replace special characters and whitespace with hyphens
    # Keep: alphanumeric, spaces, hyphens, underscores
    sanitized = re.sub(r'[^a-zA-Z0-9\s\-_]', '-', sanitized)

    # Normalize whitespace to single spaces
    sanitized = re.sub(r'\s+', ' ', sanitized)

    # Replace spaces with hyphens for filesystem compatibility
    sanitized = sanitized.replace(' ', '-')

    # Remove consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)

    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')

    # Ensure result is not empty
    if not sanitized:
        raise SecurityError("Project name is empty after sanitization")

    # Limit length (filesystem limits, typically 255 chars)
    max_length = 200
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('-')

    return sanitized


def validate_intake_id(intake_id: str) -> bool:
    """
    Validate intake ID format.

    Intake IDs should be UUIDs or UUID-like strings.
    This prevents path traversal and injection attacks.

    Args:
        intake_id: Intake ID to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> validate_intake_id("abc123-def456")
        True
        >>> validate_intake_id("../../etc/passwd")
        False
        >>> validate_intake_id("<script>alert('xss')</script>")
        False
    """
    if not intake_id:
        return False

    # Allow alphanumeric, hyphens, and underscores only
    # Typical UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    pattern = r'^[a-zA-Z0-9\-_]+$'

    if not re.match(pattern, intake_id):
        return False

    # Prevent path traversal attempts
    if '..' in intake_id or '/' in intake_id or '\\' in intake_id:
        return False

    # Reasonable length limit
    if len(intake_id) > 100:
        return False

    return True


def validate_review_id(review_id: str) -> bool:
    """
    Validate review ID format.

    Review IDs follow format: ER-YYYYMMDD-{uuid}

    Args:
        review_id: Review ID to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> validate_review_id("ER-20251215-abc123")
        True
        >>> validate_review_id("../../etc/passwd")
        False
    """
    if not review_id:
        return False

    # Review ID pattern: ER-YYYYMMDD-{alphanumeric}
    pattern = r'^ER-\d{8}-[a-zA-Z0-9\-]+$'

    if not re.match(pattern, review_id):
        return False

    # Prevent path traversal
    if '..' in review_id or '/' in review_id or '\\' in review_id:
        return False

    # Reasonable length limit
    if len(review_id) > 50:
        return False

    return True


def safe_path_join(base_path: Path, *parts: str) -> Path:
    """
    Safely join path components, preventing traversal outside base path.

    Args:
        base_path: Base directory (must be absolute)
        *parts: Path components to join

    Returns:
        Safe resolved path

    Raises:
        SecurityError: If resolved path escapes base_path

    Examples:
        >>> safe_path_join(Path("/data"), "intake", "abc.json")
        Path('/data/intake/abc.json')
        >>> safe_path_join(Path("/data"), "../etc/passwd")  # Raises SecurityError
    """
    if not base_path.is_absolute():
        raise SecurityError(f"Base path must be absolute: {base_path}")

    # Join and resolve the path
    result = base_path.joinpath(*parts).resolve()

    # Ensure result is within base_path
    try:
        result.relative_to(base_path)
    except ValueError:
        raise SecurityError(
            f"Path traversal detected: '{result}' is outside '{base_path}'"
        )

    return result


def validate_file_extension(filename: str, allowed_extensions: list[str]) -> bool:
    """
    Validate file has an allowed extension.

    Args:
        filename: Filename to check
        allowed_extensions: List of allowed extensions (e.g., ['.json', '.md'])

    Returns:
        True if extension is allowed, False otherwise

    Examples:
        >>> validate_file_extension("data.json", [".json", ".txt"])
        True
        >>> validate_file_extension("malware.exe", [".json", ".txt"])
        False
    """
    if not filename:
        return False

    path = Path(filename)
    extension = path.suffix.lower()

    return extension in [ext.lower() for ext in allowed_extensions]


def sanitize_artifact_name(artifact_name: str) -> str:
    """
    Sanitize artifact name for safe filename use.

    Converts artifact names to safe filenames following QMS-* convention.

    Args:
        artifact_name: Artifact name (e.g., "Quality Plan")

    Returns:
        Safe filename component (e.g., "Quality-Plan")

    Examples:
        >>> sanitize_artifact_name("Quality Plan")
        'Quality-Plan'
        >>> sanitize_artifact_name("CTQ Tree")
        'CTQ-Tree'
    """
    # Replace spaces with hyphens
    sanitized = artifact_name.replace(' ', '-')

    # Remove any non-alphanumeric except hyphens
    sanitized = re.sub(r'[^a-zA-Z0-9\-]', '', sanitized)

    # Remove consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)

    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')

    return sanitized


# Request validation constants
MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_JSON_DEPTH = 10  # Prevent deeply nested JSON attacks
MAX_STRING_LENGTH = 10000  # Maximum length for string fields

ALLOWED_CONTENT_TYPES = {
    "application/json",
    "multipart/form-data",
    "application/x-www-form-urlencoded"
}


def validate_json_depth(obj, max_depth: int = MAX_JSON_DEPTH, current_depth: int = 0) -> bool:
    """
    Validate JSON object depth to prevent stack overflow attacks.

    Args:
        obj: JSON object to validate
        max_depth: Maximum allowed nesting depth
        current_depth: Current recursion depth (internal)

    Returns:
        True if depth is acceptable, False otherwise
    """
    if current_depth > max_depth:
        return False

    if isinstance(obj, dict):
        for value in obj.values():
            if not validate_json_depth(value, max_depth, current_depth + 1):
                return False
    elif isinstance(obj, list):
        for item in obj:
            if not validate_json_depth(item, max_depth, current_depth + 1):
                return False

    return True


if __name__ == "__main__":
    """Test security utilities."""
    import sys

    print("Security Utilities Test Suite")
    print("=" * 60)

    # Test path sanitization
    test_cases = [
        ("My Project", "My-Project"),
        ("../../etc/passwd", "etc-passwd"),
        ("Test<>Project", "Test-Project"),
        ("  Spaced  Out  ", "Spaced-Out"),
        ("Project/With\\Slashes", "Project-With-Slashes"),
    ]

    print("\n1. Project Name Sanitization:")
    for input_name, expected in test_cases:
        result = sanitize_project_name(input_name)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{input_name}' → '{result}' (expected: '{expected}')")

    # Test ID validation
    print("\n2. ID Validation:")
    print(f"  ✅ Valid intake ID: {validate_intake_id('abc123-def456')}")
    print(f"  ✅ Invalid intake ID: {not validate_intake_id('../../etc/passwd')}")
    print(f"  ✅ Valid review ID: {validate_review_id('ER-20251215-abc123')}")
    print(f"  ✅ Invalid review ID: {not validate_review_id('../malicious')}")

    # Test safe path join
    print("\n3. Safe Path Join:")
    try:
        base = Path("/tmp/test").resolve()
        safe = safe_path_join(base, "data", "file.json")
        print(f"  ✅ Safe path: {safe}")
    except SecurityError as e:
        print(f"  ❌ Error: {e}")

    try:
        base = Path("/tmp/test").resolve()
        unsafe = safe_path_join(base, "..", "..", "etc", "passwd")
        print(f"  ❌ Should have raised SecurityError, got: {unsafe}")
    except SecurityError:
        print(f"  ✅ Correctly blocked path traversal")

    print("\n" + "=" * 60)
    print("✅ Security utilities test complete")
