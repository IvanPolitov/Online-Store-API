import os
import sys
from fastapi import FastAPI, APIRouter
import uvicorn


project_directory = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..\\.."))

if project_directory not in sys.path:
    sys.path.append(project_directory)


from api.auth import auth_router
from api.products import product_router
from api.cart import cart_router
from db.base import Base, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)

v1_router = APIRouter(prefix='/v1', tags=['v1'])
v1_router.include_router(auth_router)
v1_router.include_router(product_router)
v1_router.include_router(cart_router)


app.include_router(v1_router)


@app.get("/")
async def welcome():
    return {"message": "Welcome to Online-Store-API"}

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
