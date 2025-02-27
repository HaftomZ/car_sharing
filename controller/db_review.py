from sqlalchemy.orm.session import Session
from schemas.reviewSchema import ReviewBase
from models.Reviews import DbReview
from fastapi import HTTPException, status
from sqlalchemy.sql import func


def create_review(db: Session, request: ReviewBase, user_rating: int, receiver_id: int, creator_id: int):
    creator = db.query(DbReview).filter(DbReview.creator_id == creator_id).first()
    receiver = db.query(DbReview).filter(DbReview.receiver_id == receiver_id).first()
    if not creator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'None exist user can not create reviews')
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'None exist user can not receive reviews')
    if len(request.text_description) >= 300:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text description  cannot be more than 300 characters."
        )
    new_review = DbReview(
        rating=user_rating,
        text_description=request.text_description,
        receiver_id=receiver_id,
        creator_id=creator_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def get_review(db: Session, id: int):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Review with id {id} does not exist.')
    return review


def get_all_reviews_received(db: Session, receiver_id: int):
    review = db.query(DbReview).filter(DbReview.receiver_id == receiver_id).all()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Reviews for user_id {receiver_id} does not exist.')
    return review


def get_all_reviews_left(db: Session, creator_id: int):
    review = db.query(DbReview).filter(DbReview.creator_id == creator_id).all()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail =f'Reviews with creator_id {creator_id} does not exist.')
    return review


def update_review(db: Session, id: int, request: ReviewBase, user_rating: int, creator_id: int):
    review = db.query(DbReview).filter(DbReview.id == id)
    creator = db.query(DbReview).filter(DbReview.creator_id == creator_id).first()
    if not review.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Review with id {id} does not exist.')
    if not creator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'You do not have rights to update this review')
    if len(request.text_description) >= 300:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text description  cannot be more than 300 characters.")
    review.update({
        DbReview.rating: user_rating,
        DbReview.text_description: request.text_description,
        DbReview.created_at: func.now()
    })
    db.commit()
    return f"Review with id {id} was successfully updated."


def delete_review(db: Session, id: int, creator_id: int):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Review with id {id} does not exist.')
    if DbReview.creator_id != creator_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'You do not have rights to delete this review')
    db.delete(review)
    db.commit()
    return f"Review with id {id} was successfully deleted."
