from pydantic import BaseModel, Field
barcode_in: str = Field(..., pattern=r'^\d+$')