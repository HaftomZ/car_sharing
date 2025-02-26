from schemas.reviewSchema import ReviewBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import db_review
from schemas.reviewSchema import ReviewDisplay
from typing import List


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


# Read all reviews left for specific user_id
@router.get("/received/{receiver_id}/all", response_model=List[ReviewDisplay])
def get_review(receiver_id: int, db: Session = Depends(get_db)):
    return db_review.get_all_reviews_received(db, receiver_id)


# Read all reviews left by specific creator_id
@router.get("/left/{creator_id}/all", response_model=List[ReviewDisplay])
def get_review(creator_id: int, db: Session = Depends(get_db)):
    return db_review.get_all_reviews_left(db, creator_id)


# Update review
@router.put('/{id}/update')
def update_review(id: int, request: ReviewBase, db: Session = Depends(get_db)):
    return db_review.update_review(db, id, request)


# Delete review
@router.delete('/delete/{id}')
def delete_review(id: int, db: Session = Depends(get_db)):
    return db_review.delete_review(db, id)
