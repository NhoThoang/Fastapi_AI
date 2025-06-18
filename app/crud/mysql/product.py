from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.mysql.products import Products
from app.schemas.mysql.product import ProductBase
from fastapi import HTTPException, status

async def create_product(session: AsyncSession, product: ProductBase):
    check_barcode_exists = await session.execute(select(Products).where(Products.barcode == product.barcode))
    if check_barcode_exists.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="barcode already exists"
        )
    
    new_product = Products(**product.dict())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product

async def get_products(session: AsyncSession):
    result = await session.execute(select(Products))
    return result.scalars().all()
