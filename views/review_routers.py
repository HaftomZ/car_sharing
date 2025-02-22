from schemas.reviewSchema import ReviewBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import db_review


router = APIRouter(
    prefix="/review",
    tags=['review']
)


# Create review
@router.post("/")
def create_review(request: ReviewBase, db: Session = Depends(get_db())):
    return db_review.create_review(db, request)

# Read review
# Update review
# Delete review
