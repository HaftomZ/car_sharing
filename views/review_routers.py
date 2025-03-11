from controller.authentication import get_current_user
from schemas.adminSchema import AdminBase
from schemas.reviewSchema import ReviewBase
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import db_review
from schemas.reviewSchema import ReviewDisplay
from typing import List
from schemas.userSchema import userDisplay

router = APIRouter(
    prefix="/reviews",
    tags=['reviews']
)


# Create review
@router.post("/", response_model=ReviewDisplay, status_code=status.HTTP_201_CREATED,)
def create_review(request: ReviewBase, db: Session = Depends(get_db),
                  current_user: userDisplay = Depends(get_current_user)):
    return db_review.create_review(db, request)


@router.post("/{id}")
def upload_photos(id: int, files: list[UploadFile] = File(...), db: Session = Depends(get_db),
                  current_user: userDisplay = Depends(get_current_user)):
    return db_review.upload_photos(db, id, current_user, files)


@router.delete('/{id}/photos', status_code=status.HTTP_204_NO_CONTENT)
def delete_photos(id: int, db: Session = Depends(get_db), current_user: userDisplay = Depends(get_current_user)):
    return db_review.delete_photos(db, id, current_user)


# Read specific review
@router.get("/{id}", response_model=ReviewDisplay)
def get_review(id: int, db: Session = Depends(get_db), current_user: userDisplay = Depends(get_current_user)):
    return db_review.get_review(db, id)


# Read all reviews
@router.get("/", response_model=List[ReviewDisplay])
def get_reviews(creator_id: int = None, receiver_id: int = None, db: Session = Depends(get_db),
                current_user: userDisplay = Depends(get_current_user)):
    return db_review.get_all_reviews(db, creator_id, receiver_id)


# Update review
@router.put('/{id}')
def update_review(id: int, request: ReviewBase, db: Session = Depends(get_db),
                  current_user: userDisplay = Depends(get_current_user)):
    return db_review.update_review(db, id, request, current_user)


# Delete review
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_review(id: int, db: Session = Depends(get_db), current_user: userDisplay = Depends(get_current_user)):
    return db_review.delete_review(db, id, current_user)
