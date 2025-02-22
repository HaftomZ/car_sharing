from fastapi import FastAPI
from config.db_connect import engine
from models import Users
from views import user_routers
from views import review_routers

app = FastAPI()
app.include_router(user_routers.router)
app.include_router(review_routers.router)


@app.get('/')
def say_hello():
    return {"message:hello world"}


Users.Base.metadata.create_all(engine)
