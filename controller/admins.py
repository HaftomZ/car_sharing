from sqlalchemy.orm.session import Session
from config.Hash import Hash
from schemas.adminSchema import AdminBase
from models.Admin import DbAdmin
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status

def create_admin(db: Session, request: AdminBase, admin_role: str):
    existing_admin = db.query(DbAdmin).filter(DbAdmin.email == request.email).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists! Choose a different one."
        )    
   
    new_admin = DbAdmin(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
        role=admin_role
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Admin account has been created!, Please Log in!"}
    )

def get_all_admins(db: Session):
    admins = db.query(DbAdmin).all()
    if not admins:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No admins found!")
    return admins

def login_admin(db: Session, email: str, password: str):
    admin = db.query(DbAdmin).filter(DbAdmin.email == email).first()
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email is already exist! Create an account first!."
        )

    if not Hash.verify(admin.password, password):  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password! Incorrect password."
        )
       
    return admin 


def update_admin(db: Session, id:int, request: AdminBase, admin_role: str):    
    admin = db.query(DbAdmin).filter(DbAdmin.id == id)
    if not admin.first():
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail = f'admin with id {id} is not exist!')
    admin.update({        
        DbAdmin.username : request.username,
        DbAdmin.email: request.email,
        DbAdmin.password: Hash.bcrypt(request.password),  
        DbAdmin.role: admin_role ,             
    })
    db.commit()
    return 'admin information has been updated successfully!'

def delete_admin(db: Session, id: int):
    admin = db.query(DbAdmin).filter(DbAdmin.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found!")
    
    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted successfully!"}
