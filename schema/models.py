from typing import List

from pydantic import BaseModel


class DeepLearningModel(BaseModel):
    confidence_threshold: float
    iou_threshold: float = 0.5
    labels: List[str]


class ObjectDetectionModel(DeepLearningModel):
    pass

class Detectron2Model(DeepLearningModel):
    weights = dict
    config = dict
    confidence_threshold: float
    iou_threshold: float = 0.5
    labels: List[str]
