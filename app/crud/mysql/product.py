from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.mysql.products import Products, Product_images
from app.schemas.mysql.product import ProductBase, Image_hash
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

async def create_product(session: AsyncSession, product: ProductBase)-> Products:
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
async def insert_image_url_image_hash(session: AsyncSession, image_hash: Image_hash)-> Product_images:
    new_image = Product_images(**image_hash.dict())
    session.add(new_image)
    await session.commit()
    await session.refresh(new_image)
    return new_image
async def check_image_hash_exists(session: AsyncSession, image_hash: str)-> Product_images:
    result = await session.execute(select(Product_images).where(Product_images.image_hash == image_hash))
    return result.scalars().first()


async def check_image_hash_and_username_exists(session: AsyncSession, username: str, barcode: str, image_hash: str) -> Product_images | None:
    result = await session.execute(
        select(Product_images).where(
            Product_images.username == username,
            Product_images.barcode == barcode,
            Product_images.image_hash == image_hash
        )
    )
    return result.scalars().first() 

def get_product_by_barcode(session: AsyncSession, barcode: str):
    return session.execute(select(Products).options(selectinload(Products.images)).where(Products.barcode == barcode)).scalar()

async def get_products(session: AsyncSession):
    result = await session.execute(select(Products))
    return result.scalars().all()
