# from typing import Dict, List, Literal, Union
# from pydantic import BaseModel, Field

# # ----- Các khối mô tả ----- #
# class DescriptionText(BaseModel):
#     type: Literal["text"]
#     content: str

# class DescriptionImage(BaseModel):
#     type: Literal["image"]
#     url: str

# class DescriptionSpecs(BaseModel):
#     type: Literal["specs"]
#     items: Dict[str, str]

# class DescriptionVideo(BaseModel):
#     type: Literal["video"]
#     url: str

# DescriptionBlock = Union[
#     DescriptionText,
#     DescriptionImage,
#     DescriptionSpecs,
#     DescriptionVideo,
# ]

# # ----- Thông tin SEO ----- #
# class SEO(BaseModel):
#     title: str | None = None
#     description: str | None = None
#     tags: List[str] = Field(default_factory=list)
