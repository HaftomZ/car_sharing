from sqlalchemy.orm.session import Session
from schemas.reviewSchema import ReviewBase
from models.Reviews import DbReview
from fastapi import HTTPException, status

def create_review(db: Session, request: ReviewBase):
    new_review = DbReview(
        mark=request.mark,
        text_description=request.text_description,
        user_id=request.creator_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def get_review(db: Session, id: int):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    # Handle errors
    if not review:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail = f'review with id {id} is not exist!')
    return review
