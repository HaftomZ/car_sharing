from sqlalchemy.orm.session import Session
from schemas.reviewSchema import ReviewBase
from models.Reviews import DbReview
from fastapi import HTTPException, status
from sqlalchemy.sql import func


def create_review(db: Session, request: ReviewBase):
    new_review = DbReview(
        rating=request.rating,
        text_description=request.text_description,
        receiver_id=request.receiver_id,
        creator_id=request.creator_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def get_review(db: Session, id: int):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Review with id {id} does not exist!')
    return review


def get_all_reviews_received(db: Session, receiver_id: int):
    review = db.query(DbReview).filter(DbReview.receiver_id == receiver_id).all()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Review for user_id {receiver_id} does not exist!')
    return review


def get_all_reviews_left(db: Session, creator_id: int):
    review = db.query(DbReview).filter(DbReview.creator_id == creator_id).all()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail =f'Review with creator_id {creator_id} does not exist!')
    return review


def update_review(db: Session, id: int, request: ReviewBase):
    review = db.query(DbReview).filter(DbReview.id == id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Review with id {id} does not exist!')
    review.update({
        DbReview.rating: request.rating,
        DbReview.text_description: request.text_description,
        DbReview.created_at: func.now()
    })
    db.commit()
    return 'ok'


def delete_review(db: Session, id: int):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Review with id {id} does not exist!')
    db.delete(review)
    db.commit()
    return "ok"
