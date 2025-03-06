from fastapi import APIRouter , HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from config.db_connect import get_db
from config import Hash , oauth2
from models import Users
from controller import authentication

router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
def create_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   return authentication.create_token(request , db)