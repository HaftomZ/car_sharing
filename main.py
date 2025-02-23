from fastapi import FastAPI
from config.db_connect import engine
from models import Users, Cars, Booking, Reviews
from views import user_routers, booking_routers, car_routers, review_routers,trip_routers

app = FastAPI()
app.include_router(user_routers.router)
app.include_router(booking_routers.router)
app.include_router(trip_routers.router)
app.include_router(car_routers.router)
app.include_router(review_routers.router)
@app.get('/')
def say_hello():
    return {"message:hello world"}

Users.Base.metadata.create_all(engine)
