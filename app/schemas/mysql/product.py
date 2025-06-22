from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name_product: str
    barcode: str = Field(..., pattern=r'^\d+$')
    quantity: int
    import_price: int
    sell_price: int
    discount: int
    expiry_date: datetime
    type_product: str
class Image_hash(BaseModel):
    username: str
    barcode:str 
    image_hash: str
    image_url: str
class OutputImage_hash(Image_hash):
    model_config = ConfigDict(from_attributes=True)
  
class ProductOut(ProductBase):
    id: int
    input_date: datetime
    model_config = ConfigDict(from_attributes=True)

class ProductWithImage(BaseModel):
    name_product: str
    barcode: str
    quantity: int
    sell_price: int
    discount: int
    image_url: list[str]   

    # class Config:
    #     from_attributes = True
        # model_config = ConfigDict(from_attributes=True)
