from sqlalchemy.orm.session import Session
from config.Hash import Hash
from schemas.adminSchema import AdminBase
from models.Admin import DbAdmin, AdminRole
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status

def create_admin(db: Session, request: AdminBase):
    existing_admin = db.query(DbAdmin).filter(DbAdmin.email == request.email).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists! Choose a different one."
        )
    
    try:
        role_enum = AdminRole(request.role.lower()) 
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role provided")

    new_admin = DbAdmin(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
        role=role_enum
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Admin account has been created!"}
    )

def get_all_admins(db: Session):
    admins = db.query(DbAdmin).all()
    if not admins:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No admins found!")
    return admins

def delete_admin(db: Session, id: int):
    admin = db.query(DbAdmin).filter(DbAdmin.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found!")
    
    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted successfully!"}
