from sqlalchemy.orm.session import Session
from schemas.reviewSchema import ReviewBase
from models.Reviews import DbReview


def create_review(db: Session, request: ReviewBase):
    new_review = DbReview(
        mark=request.mark,
        text_description=request.text_description
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

