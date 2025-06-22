from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.mysql.products import Products, Product_images
from app.schemas.mysql.product import ProductBase, Image_hash, ProductWithImage
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import exists


async def check_barcode_exists(session: AsyncSession, barcode: str) -> bool:
    print(barcode)
    stmt = select(exists().where(Products.barcode == barcode))
    result = await session.execute(stmt)
    return result.scalar()
async def create_product(session: AsyncSession, product: ProductBase)-> Products:
    if await check_barcode_exists(session, product.barcode):
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
async def get_product_by_barcode(session: AsyncSession, barcode: str):
    result = await session.execute(
        select(
            Products.name_product,
            Products.barcode,
            Products.quantity,
            Products.sell_price,
            Products.discount,
            Product_images.image_url
        )
        .join(Product_images, Products.barcode == Product_images.barcode)
        .where(Products.barcode == barcode)
    )
    rows = result.all()
    if not rows:
        return None
    first_row = rows[0]
    image_urls = [row[5] for row in rows]  # lấy image_url từ mỗi dòng
    return ProductWithImage(
        name_product=first_row[0],
        barcode=first_row[1],
        quantity=first_row[2],
        sell_price=first_row[3],
        discount=first_row[4],
        image_url=image_urls
    )

# async def get_product_by_barcode(session: AsyncSession, barcode: str):
#     result = await session.execute(
#         select(Products)
#         .options(selectinload(Products.images))
#         .where(Products.barcode == barcode)
#     )
#     return result.scalars().first()
# async def get_product_by_barcode(session: AsyncSession, barcode: str):
#     result = await session.execute(
#         select(Products)
#         .options(selectinload(Products.images))
#         .where(Products.barcode == barcode)
#     )
#     product = result.scalars().first()
    
#     # Lọc lại chỉ lấy các field mong muốn từ bảng con
#     if product:
#         product.images = [
#             {"image_url": img.image_url, "create_date": img.create_date}
#             for img in product.images
#         ]
    
#     return product


async def get_products(session: AsyncSession):
    result = await session.execute(select(Products))
    return result.scalars().all()
