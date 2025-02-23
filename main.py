from fastapi import FastAPI
from config.db_connect import engine
from models import Users
<<<<<<< HEAD
from views import user_routers, booking_routers

app = FastAPI()
app.include_router(user_routers.router)
app.include_router(booking_routers.router)
from models import Users , Cars
from views import user_routers , car_routers

app = FastAPI()
app.include_router(user_routers.router)
app.include_router(car_routers.router)

=======
from views import user_routers
from views import review_routers

app = FastAPI()
app.include_router(user_routers.router)
app.include_router(review_routers.router)
>>>>>>> reviews_schema


@app.get('/')
def say_hello():
    return {"message:hello world"}


Users.Base.metadata.create_all(engine)
