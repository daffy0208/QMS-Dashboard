"""
Runtime Configuration for QMS Dashboard
Phase 7 WS-1: Environment Hardening

Provides centralized, validated configuration from environment variables.
Fail-fast on invalid configuration in production mode.
"""

import os
import sys
from pathlib import Path
from typing import Literal

# Valid environment names
Environment = Literal["development", "verification", "production"]


class ConfigurationError(Exception):
    """Raised when configuration is invalid or incomplete."""
    pass


class RuntimeConfig:
    """
    Centralized runtime configuration.

    Environment Variables:
    - QMS_ENV: Environment name (development|verification|production)
    - QMS_DATA_ROOT: Absolute path to data root directory
    - QMS_LOG_LEVEL: Logging level (DEBUG|INFO|WARNING|ERROR)
    - QMS_HOST: Server bind address (default: 0.0.0.0)
    - QMS_PORT: Server port (default: 8000)
    - QMS_CORS_ORIGINS: Comma-separated allowed CORS origins (default: * in dev)
    """

    def __init__(self):
        """Load and validate configuration from environment."""
        self._load_environment()
        self._validate_configuration()
        self._ensure_directories()

    def _load_environment(self):
        """Load configuration from environment variables."""
        # Environment name
        self.env: Environment = os.getenv("QMS_ENV", "development")
        if self.env not in ("development", "verification", "production"):
            raise ConfigurationError(
                f"Invalid QMS_ENV='{self.env}'. "
                f"Must be: development, verification, or production"
            )

        # Data root directory
        data_root_env = os.getenv("QMS_DATA_ROOT")
        if data_root_env:
            self.data_root = Path(data_root_env).resolve()
        else:
            # Default: project root / data
            project_root = Path(__file__).parent.parent.parent
            self.data_root = project_root / "data"

        # Logging level
        self.log_level = os.getenv("QMS_LOG_LEVEL", "INFO")
        if self.log_level not in ("DEBUG", "INFO", "WARNING", "ERROR"):
            raise ConfigurationError(
                f"Invalid QMS_LOG_LEVEL='{self.log_level}'. "
                f"Must be: DEBUG, INFO, WARNING, or ERROR"
            )

        # Server configuration
        self.host = os.getenv("QMS_HOST", "0.0.0.0")
        self.port = int(os.getenv("QMS_PORT", "8000"))

        # CORS origins
        cors_env = os.getenv("QMS_CORS_ORIGINS")
        if cors_env:
            self.cors_origins = [origin.strip() for origin in cors_env.split(",")]
        else:
            # Default: wildcard in development, deny in production
            if self.env == "development":
                self.cors_origins = ["*"]
            else:
                self.cors_origins = []  # Must be explicitly configured

    def _validate_configuration(self):
        """Validate configuration is complete and sensible."""
        errors = []

        # Production requires explicit data root
        if self.env == "production" and not os.getenv("QMS_DATA_ROOT"):
            errors.append(
                "QMS_ENV=production requires explicit QMS_DATA_ROOT "
                "(no default paths in production)"
            )

        # Production requires CORS configuration
        if self.env == "production" and not self.cors_origins:
            errors.append(
                "QMS_ENV=production requires QMS_CORS_ORIGINS "
                "(wildcard CORS not allowed in production)"
            )

        # Port must be valid
        if not (1 <= self.port <= 65535):
            errors.append(f"Invalid QMS_PORT={self.port}. Must be 1-65535")

        if errors:
            raise ConfigurationError(
                "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            )

    def _ensure_directories(self):
        """Ensure required directories exist and are writable."""
        # Verify data root is writable
        if not self.data_root.exists():
            try:
                self.data_root.mkdir(parents=True, exist_ok=True)
            except PermissionError as e:
                raise ConfigurationError(
                    f"Cannot create data root directory: {self.data_root}\n"
                    f"Error: {e}"
                )

        if not os.access(self.data_root, os.W_OK):
            raise ConfigurationError(
                f"Data root directory is not writable: {self.data_root}"
            )

        # Create subdirectories
        self.intake_dir = self.data_root / "intake-responses"
        self.reviews_dir = self.data_root / "reviews"
        self.artifacts_dir = self.data_root / "artifacts"

        for directory in [self.intake_dir, self.reviews_dir, self.artifacts_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def get_intake_path(self, intake_id: str) -> Path:
        """Get path to intake response file."""
        return self.intake_dir / f"{intake_id}.json"

    def get_review_path(self, review_id: str, response: bool = False) -> Path:
        """Get path to review request or response file."""
        if response:
            return self.reviews_dir / f"{review_id}_response.json"
        else:
            return self.reviews_dir / f"{review_id}.json"

    def get_artifacts_path(self, intake_id: str) -> Path:
        """Get path to artifacts directory for an intake."""
        return self.artifacts_dir / intake_id

    def get_review_log_path(self) -> Path:
        """Get path to Expert-Review-Log.md."""
        return self.data_root / "Expert-Review-Log.md"

    def summary(self) -> str:
        """Generate configuration summary for logging."""
        return f"""QMS Dashboard Runtime Configuration
Environment: {self.env}
Data Root: {self.data_root}
  - Intake Responses: {self.intake_dir}
  - Reviews: {self.reviews_dir}
  - Artifacts: {self.artifacts_dir}
  - Review Log: {self.get_review_log_path()}
Server: {self.host}:{self.port}
CORS Origins: {', '.join(self.cors_origins) if self.cors_origins else 'NONE (deny all)'}
Log Level: {self.log_level}
"""


# Global configuration instance
_config: RuntimeConfig = None


def get_config() -> RuntimeConfig:
    """
    Get or create global configuration instance.

    Raises:
        ConfigurationError: If configuration is invalid
    """
    global _config
    if _config is None:
        _config = RuntimeConfig()
    return _config


def validate_configuration() -> None:
    """
    Validate configuration and print summary.
    Call this on application startup.

    Raises:
        ConfigurationError: If configuration is invalid
    """
    config = get_config()
    print("[CONFIG] " + "=" * 60)
    print(config.summary())
    print("[CONFIG] " + "=" * 60)


if __name__ == "__main__":
    """Test configuration validation."""
    try:
        validate_configuration()
        print("\n✅ Configuration valid")
    except ConfigurationError as e:
        print(f"\n❌ Configuration error:\n{e}", file=sys.stderr)
        sys.exit(1)
