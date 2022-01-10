from typing import List
import numpy as np

from pydantic import BaseModel
from pydantic import validator

from schema.annotations import COCOLabel

class Image(BaseModel):
    height: int
    width: int
    values: np.ndarray

    @validator('values', pre=True)
    def parse_values(v):
        return np.array(v, dtype=float)

    class Config:
        arbitrary_types_allowed = True


class RawImageList(BaseModel):
    __root__: List[Image]

class MaskAnnotatedImageList(BaseModel):
    images: RawImageList
    labels : List[COCOLabel]

class BboxAnnotatedImageList(BaseModel):
    pass