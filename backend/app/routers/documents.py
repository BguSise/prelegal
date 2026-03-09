from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.services.document_service import (
    list_documents,
    get_document,
    create_document,
    update_document,
    delete_document,
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=list[DocumentResponse])
def list_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all documents for the current user."""
    documents = list_documents(db, current_user.id)
    return documents


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_new_document(
    request: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new document."""
    document = create_document(db, current_user.id, request)
    return document


@router.get("/{document_id}", response_model=DocumentResponse)
def get_user_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific document."""
    document = get_document(db, document_id, current_user.id)
    return document


@router.put("/{document_id}", response_model=DocumentResponse)
def update_user_document(
    document_id: int,
    request: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a document."""
    document = update_document(db, document_id, current_user.id, request)
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a document."""
    delete_document(db, document_id, current_user.id)
    return None
