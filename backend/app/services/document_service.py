from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.services.template_service import get_template


def list_documents(db: Session, user_id: int) -> list[Document]:
    """List all documents for a user."""
    return db.query(Document).filter(Document.user_id == user_id).all()


def get_document(db: Session, document_id: int, user_id: int) -> Document:
    """Get a specific document, ensuring user ownership."""
    # Combine conditions to prevent enumeration attacks (404 vs 403 distinction)
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id
    ).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return document


def create_document(db: Session, user_id: int, data: DocumentCreate) -> Document:
    """Create a new document."""
    # Validate template exists
    get_template(data.template_id)

    # Create document
    document = Document(
        user_id=user_id,
        template_id=data.template_id,
        title=data.title,
        field_values=data.field_values,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def update_document(db: Session, document_id: int, user_id: int, data: DocumentUpdate) -> Document:
    """Update a document."""
    document = get_document(db, document_id, user_id)

    if data.title is not None:
        document.title = data.title
    if data.field_values is not None:
        document.field_values = data.field_values
    if data.status is not None:
        document.status = data.status

    db.commit()
    db.refresh(document)
    return document


def delete_document(db: Session, document_id: int, user_id: int) -> None:
    """Delete a document."""
    document = get_document(db, document_id, user_id)
    db.delete(document)
    db.commit()
