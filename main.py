from fastapi import FastAPI, Depends
from config.db_connect import engine
from models import Users, Cars
from views import (user_routers, car_routers, review_routers, booking_routers, trip_routers, authentication_routers,
                   payment_routers, reports_routers)
from config.db_connect import get_db
from sqlalchemy.orm import Session
from controller import users


app = FastAPI()


@app.get("/verifications/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    return users.verify_email(token, db)


app.include_router(authentication_routers.router)
app.include_router(user_routers.router)
app.include_router(booking_routers.router)
app.include_router(trip_routers.router)
app.include_router(car_routers.router)
app.include_router(review_routers.router)
app.include_router(payment_routers.router)
# app.include_router(reports_routers.router)


@app.get('/')
def welcome():
    return {"message:Welcome to HRIN app!, use /docs to use the app!"}


Users.Base.metadata.create_all(engine)

