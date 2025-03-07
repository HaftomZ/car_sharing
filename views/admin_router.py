from schemas.adminSchema import AdminBase, AdminDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import admins

router = APIRouter(
    prefix="/admins",
    tags=["admins"]
)

@router.post("/", response_model=AdminDisplay)
def create_admin(req: AdminBase, db: Session = Depends(get_db)):
    return admins.create_admin(db, req)

@router.get("/", response_model=list[AdminDisplay])
def get_all_admins(db: Session = Depends(get_db)):
    return admins.get_all_admins(db)

@router.delete("/{id}")
def delete_admin(id: int, db: Session = Depends(get_db)):
    return admins.delete_admin(db, id)
