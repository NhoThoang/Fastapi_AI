from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import  ProductOut, ProductBase
from app.crud import product as crud_product
from app.db.session import get_db
from fastapi import status
router = APIRouter()

@router.post("/products/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductBase, session: AsyncSession = Depends(get_db)):
    return await crud_product.create_product(session, product)

@router.get("/products/", response_model=list[ProductOut], status_code=status.HTTP_200_OK)
async def get_all_products(session: AsyncSession = Depends(get_db)):
    return await crud_product.get_products(session)
