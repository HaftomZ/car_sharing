from fastapi import FastAPI
from config.db_connect import engine
from models import Users , Cars
from views import user_routers , car_routers, review_routers, booking_routers, trip_routers, authentication_routers, admin_router,payment_routers , reports_routers





app = FastAPI()
app.include_router(authentication_routers.router)
app.include_router(admin_router.router) 
app.include_router(user_routers.router)
app.include_router(booking_routers.router)
app.include_router(trip_routers.router)
app.include_router(car_routers.router)
app.include_router(review_routers.router)
app.include_router(payment_routers.router)
app.include_router(reports_routers.router)



@app.get('/')
def welcome():
    return {"message:Welcome to HRIN app!, use /docs to use the app!"}

Users.Base.metadata.create_all(engine)
