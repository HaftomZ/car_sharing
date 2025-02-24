from schemas.reviewSchema import ReviewBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import db_review
from schemas.reviewSchema import ReviewDisplay


router = APIRouter(
    prefix="/review",
    tags=['review']
)


# Create review
@router.post("/", response_model=ReviewDisplay)
def create_review(request: ReviewBase, db: Session = Depends(get_db)):
    return db_review.create_review(db, request)


# Read specific review
@router.get("/{id}", response_model=ReviewDisplay)
def get_review(id: int, db: Session = Depends(get_db)):
    return db_review.get_review(db, id)


# Read all reviews
@router.get("/{id}", response_model=ReviewDisplay)
def get_review(id: int, db: Session = Depends(get_db)):
    return db_review.get_review(db, id)


# Update review
@router.post('/{id}/update')
def update_review(id: int, request: ReviewBase, db: Session = Depends(get_db())):
    return db_review.update_review(db, id, request)


# Delete review
@router.get('/delete/{id}')
def delete_review(id: int, db: Session = Depends(get_db())):
    return db_review.delete_review(db, id)
