from enum import Enum
from schemas.adminSchema import AdminBase, AdminDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import admins

router = APIRouter(
    prefix="/admins",
    tags=["admins"]
)

class AdminRole(str, Enum):
    super_admin = "super_admin"
    moderator = "moderator"

@router.post("/", response_model=AdminDisplay)
def create_admin(admin_role: AdminRole,req: AdminBase, db: Session = Depends(get_db)):
    return admins.create_admin(db, req, admin_role.value)

@router.get("/", response_model=list[AdminDisplay])
def get_all_admins(db: Session = Depends(get_db)):
    return admins.get_all_admins(db)

@router.get('/{id}', response_model=AdminDisplay)
def get_admin(email: str, password: str, db: Session = Depends(get_db)):
    return admins.login_admin(db, email, password)

@router.put('/{id}')
def update_admin(admin_role: AdminRole, id: int, request: AdminBase, db: Session = Depends(get_db)):
    return admins.update_admin(db, id, request, admin_role.value )

@router.delete("/{id}")
def delete_admin(id: int, db: Session = Depends(get_db)):
    return admins.delete_admin(db, id)
