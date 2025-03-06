from sqlalchemy.orm.session import Session
from schemas.reviewSchema import ReviewBase
from models.Reviews import DbReview
from fastapi import HTTPException, status, File, UploadFile, Form
from sqlalchemy.sql import func
from models.Users import DbUser
from pathlib import Path
from config.pictures_handler import upload_picture
from typing import Optional

UPLOAD_DIR = Path("reviews_photos")
UPLOAD_DIR.mkdir(exist_ok=True)


def create_review(db: Session, user_rating: int, receiver_id: int, creator_id: int,
                  text_description: Optional[str] = Form(None), files: Optional[list[UploadFile]] = File(None)):
    creator = db.query(DbUser).filter(DbUser.id == creator_id).first()
    receiver = db.query(DbUser).filter(DbUser.id == receiver_id).first()
    if not creator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'None exist user can not create reviews')
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'None exist user can not receive reviews')
    if creator_id == receiver_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail=f'You can not leave review about yourself.')
    if len(text_description) >= 300:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text description cannot be more than 300 characters."
        )
    file_paths = []
    if files:
        for file in files:
            final_path = upload_picture(UPLOAD_DIR, file)
            file_paths.append(str(final_path))
    photos = ",".join(file_paths)
    new_review = DbReview(
        rating=user_rating,
        text_description=text_description,
        receiver_id=receiver_id,
        creator_id=creator_id,
        photos=photos
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def get_review(db: Session, id: int):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return review


def get_all_reviews(db: Session, creator_id: int, receiver_id: int):
    review_query = db.query(DbReview)
    if creator_id is not None:
        review_query = review_query.filter(DbReview.creator_id == creator_id)
    if receiver_id is not None:
        review_query = review_query.filter(DbReview.receiver_id == receiver_id)
    return review_query.all()


def update_review(db: Session, id: int, request: ReviewBase, user_rating: int, creator_id: int, receiver_id: int):
    review = db.query(DbReview).filter(DbReview.id == id)
    creator = db.query(DbReview).filter(DbReview.creator_id == creator_id)
    if not review.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not creator.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f'You do not have rights to update this review')
    if len(request.text_description) >= 300:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text description  cannot be more than 300 characters.")
    review.update({
        DbReview.rating: user_rating,
        DbReview.text_description: request.text_description,
        DbReview.created_at: func.now(),
        DbReview.receiver_id: receiver_id
    })
    db.commit()
    return review


def delete_review(db: Session, id: int, creator_id: int):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    creator = db.query(DbReview).filter(DbReview.creator_id == creator_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Review with id {id} does not exist.')
    if not creator:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f'You do not have rights to delete this review')
    db.delete(review)
    db.commit()
    return f"Review with id {id} was successfully deleted."


def upload_photos(db: Session, id: int, files: list[UploadFile] = File(...)):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    file_paths = []
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for file in files:
        final_path = upload_picture(UPLOAD_DIR, file)
        file_paths.append(str(final_path))
    if review.photos:
        existing_photos = review.photos.split(",")
        review.photos = ",".join(existing_photos + file_paths)
    else:
        review.photos = ",".join(file_paths)
    db.commit()
    db.refresh(review)
    return review
