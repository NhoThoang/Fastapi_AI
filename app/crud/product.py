from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.products import Products
from app.schemas.product import ProductBase

async def create_product(session: AsyncSession, product: ProductBase):
    new_product = Products(**product.dict())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product

async def get_products(session: AsyncSession):
    result = await session.execute(select(Products))
    return result.scalars().all()
