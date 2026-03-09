from fastapi import APIRouter

from app.services.template_service import get_catalog, get_template

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("")
def list_templates():
    """Get the catalog of all available templates."""
    return get_catalog()


@router.get("/{template_id}")
def get_template_detail(template_id: str):
    """Get a specific template by ID."""
    return get_template(template_id)
