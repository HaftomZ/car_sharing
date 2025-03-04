from enum import Enum
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


class UserRating(int, Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

# Create review
@router.post("/", response_model=ReviewDisplay)
def create_review(request: ReviewBase, user_rating: UserRating, receiver_id: int, creator_id: int, db: Session = Depends(get_db)):
    return db_review.create_review(db, request, user_rating, receiver_id, creator_id)


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
def update_review(id: int, request: ReviewBase, receiver_id: int, user_rating: UserRating, creator_id: int, db: Session = Depends(get_db)):
    return db_review.update_review(db, id, request, user_rating, creator_id, receiver_id)


# Delete review
@router.delete('/delete/{id}')
def delete_review(id: int, creator_id: int, db: Session = Depends(get_db)):
    return db_review.delete_review(db, id, creator_id)
