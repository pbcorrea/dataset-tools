from typing import List
from typing import Tuple
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class Polygon(BaseModel):
    vertices: List[Tuple[float]]


class Bbox(BaseModel):
    x: float
    y: float
    width: float
    height: float


class COCOAnnotation(BaseModel):
    id: int
    image_id: int
    category_id: int
    segmentation: Polygon
    area: float
    bbox: Bbox
    iscrowd: int


class COCOImage(BaseModel):
    id: int
    width: int
    height: int
    file_name: str
    license: Optional[int] = 0
    flickr_url: Optional[str]
    coco_url: Optional[str]
    date_captured: datetime


class COCOCategories(BaseModel):
    id: int
    name: str
    supercategory: str


class COCOLabel(BaseModel):
    annotation: COCOAnnotation
    image: COCOImage
    categories: COCOCategories


class InstanceSegmentationAnnotationList(BaseModel):
    __root__: List[COCOLabel]