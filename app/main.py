from fastapi import FastAPI
# from app.api.v1 import routes_user, routes_product
from app.api.v1 import routes_product, routes_create_account, routes_login
from app.db.mongo.session_mongo import init_db
from app.core.middlewares import setup_middlewares
from app.core.config import config_app
# import logging


app = FastAPI(title="My FastAPI App", debug=config_app.debug)
setup_middlewares(app)
app.include_router(routes_login.router, prefix="/api/v1", tags=["Login"])
app.include_router(routes_create_account.router, prefix="/api/v1", tags=["Create Account"])
app.include_router(routes_product.router, prefix="/api/v1", tags=["Product"])

@app.on_event("startup")
async def startup_event():
    await init_db()
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)




# from fastapi import FastAPI

# app = FastAPI()

# Import and include routers here
# from app.api.v1.routes_user import router as user_router
# from app.api.v1.routes_auth import router as auth_router
# app.include_router(user_router, prefix="/api/v1/users")
# app.include_router(auth_router, prefix="/api/v1/auth")