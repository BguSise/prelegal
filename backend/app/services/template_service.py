import json
from pathlib import Path
from fastapi import HTTPException, status

from app.config import settings


def _validate_template_path(template_path: Path) -> None:
    """Prevent path traversal attacks by ensuring the resolved path is within templates_dir."""
    base = Path(settings.templates_dir).resolve()
    resolved = template_path.resolve()

    # Ensure the resolved path starts with the base directory
    try:
        resolved.relative_to(base)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid template ID",
        )


def get_catalog() -> list[dict]:
    """Load and return the template catalog."""
    catalog_path = Path(settings.templates_dir) / "index.json"
    try:
        with open(catalog_path, "r") as f:
            data = json.load(f)
        return data.get("templates", [])
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template catalog not found",
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse template catalog",
        )


def get_template(template_id: str) -> dict:
    """Load a specific template by ID with path traversal protection."""
    template_path = Path(settings.templates_dir) / f"{template_id}.json"

    # Prevent path traversal attacks
    _validate_template_path(template_path)

    try:
        with open(template_path, "r") as f:
            template = json.load(f)
        return template
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_id}' not found",
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse template '{template_id}'",
        )
