"""
Artifact Generator - Phase 4

Generates QMS artifacts based on risk classification and intake answers.
Creates context-aware, first-pass content (not just empty templates).
Phase 7 WS-1: Uses centralized configuration.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.intake import IntakeRequest, IntakeResponse, RiskClassification
from config import get_config
from security import sanitize_project_name, sanitize_artifact_name


class ArtifactGenerator:
    """
    Main artifact generation engine.

    Responsibilities:
    1. Determine which artifacts are required based on risk level
    2. Generate artifacts with project-specific content
    3. Create Markdown files
    4. Return artifact metadata
    """

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_artifacts(
        self,
        intake_request: IntakeRequest,
        intake_response: IntakeResponse
    ) -> Dict[str, any]:
        """
        Generate all required QMS artifacts for the given intake.

        Returns:
            {
                "artifacts_generated": ["Quality Plan", "CTQ Tree", ...],
                "file_paths": ["QMS-Quality-Plan.md", ...],
                "output_directory": "/path/to/artifacts",
                "zip_file": "/path/to/artifacts.zip"
            }
        """
        risk_level = intake_response.classification.risk_level
        required_artifacts = self._get_required_artifacts(risk_level)

        generated_files = []
        artifact_names = []

        # Generate each required artifact
        for artifact_name in required_artifacts:
            content = self._generate_artifact_content(
                artifact_name,
                intake_request,
                intake_response
            )

            file_path = self._write_artifact_file(artifact_name, content)
            generated_files.append(file_path)
            artifact_names.append(artifact_name)

        # Create ZIP archive
        zip_path = self._create_zip_archive(generated_files, intake_request.project_name)

        return {
            "artifacts_generated": artifact_names,
            "file_paths": [str(f) for f in generated_files],
            "output_directory": str(self.output_dir),
            "zip_file": str(zip_path)
        }

    def _get_required_artifacts(self, risk_level: str) -> List[str]:
        """
        Return list of required artifacts based on risk level.

        Per intake-rules.md:70-88:
        - R0: 5 artifacts (base)
        - R1: 8 artifacts (base + 3)
        - R2/R3: 11 artifacts (base + 3 + 3)
        """
        base_artifacts = [
            "Quality Plan",
            "CTQ Tree",
            "Assumptions Register",
            "Risk Register",
            "Traceability Index"
        ]

        r1_artifacts = [
            "Verification Plan",
            "Validation Plan",
            "Measurement Plan"
        ]

        r2_artifacts = [
            "Control Plan",
            "Change Log",
            "CAPA Log"
        ]

        if risk_level == "R0":
            return base_artifacts
        elif risk_level == "R1":
            return base_artifacts + r1_artifacts
        elif risk_level in ["R2", "R3"]:
            return base_artifacts + r1_artifacts + r2_artifacts
        else:
            return base_artifacts

    def _generate_artifact_content(
        self,
        artifact_name: str,
        intake_request: IntakeRequest,
        intake_response: IntakeResponse
    ) -> str:
        """
        Generate content for a specific artifact.
        Uses templates and populates with project-specific content.
        """
        # Import artifact templates
        from artifacts.templates import (
            quality_plan,
            ctq_tree,
            assumptions_register,
            risk_register,
            traceability_index,
            verification_plan,
            validation_plan,
            measurement_plan,
            control_plan,
            change_log,
            capa_log
        )

        template_map = {
            "Quality Plan": quality_plan.generate,
            "CTQ Tree": ctq_tree.generate,
            "Assumptions Register": assumptions_register.generate,
            "Risk Register": risk_register.generate,
            "Traceability Index": traceability_index.generate,
            "Verification Plan": verification_plan.generate,
            "Validation Plan": validation_plan.generate,
            "Measurement Plan": measurement_plan.generate,
            "Control Plan": control_plan.generate,
            "Change Log": change_log.generate,
            "CAPA Log": capa_log.generate
        }

        generator_func = template_map.get(artifact_name)
        if not generator_func:
            raise ValueError(f"Unknown artifact: {artifact_name}")

        return generator_func(intake_request, intake_response)

    def _write_artifact_file(self, artifact_name: str, content: str) -> Path:
        """
        Write artifact content to Markdown file.

        File naming: QMS-{ArtifactName}.md
        Example: QMS-Quality-Plan.md

        Phase 7 WS-2: Uses sanitize_artifact_name() for security.
        """
        # Phase 7 WS-2: Sanitize artifact name for safe filesystem use
        safe_name = sanitize_artifact_name(artifact_name)
        filename = f"QMS-{safe_name}.md"
        file_path = self.output_dir / filename

        with open(file_path, 'w') as f:
            f.write(content)

        return file_path

    def _create_zip_archive(
        self,
        file_paths: List[Path],
        project_name: str
    ) -> Path:
        """
        Create ZIP archive containing all generated artifacts.

        Phase 7 WS-2: Uses sanitize_project_name() for security.
        """
        import zipfile

        # Phase 7 WS-2: Sanitize project name using security utilities
        safe_name = sanitize_project_name(project_name)

        zip_filename = f"{safe_name}-QMS-Artifacts.zip"
        zip_path = self.output_dir / zip_filename

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                # Add file to ZIP with just the filename (no path)
                zipf.write(file_path, file_path.name)

        return zip_path


def generate_project_artifacts(
    intake_request: IntakeRequest,
    intake_response: IntakeResponse,
    output_dir: str | Path = None
) -> Dict[str, any]:
    """
    Convenience function to generate artifacts for a project.

    Args:
        intake_request: Original intake request
        intake_response: Classification response with warnings
        output_dir: Where to save artifacts (default: config.artifacts_dir/{intake_id})

    Returns:
        Dictionary with generated files and metadata
    """
    if output_dir is None:
        # Phase 7 WS-1: Use centralized config
        config = get_config()
        output_dir = config.get_artifacts_path(intake_response.intake_id)
    else:
        output_dir = Path(output_dir)

    generator = ArtifactGenerator(output_dir)
    return generator.generate_artifacts(intake_request, intake_response)
