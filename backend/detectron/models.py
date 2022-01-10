from detectron2 import model_zoo
from detectron2.config import get_cfg
from create_dataset.utils.labels import COCO_LABELS

class MaskRCNN:
    def __init__(self, checkpoint:str="COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml", confidence_threshold:float=0.5):
        self.config = get_cfg().merge_from_file(model_zoo.get_config_file(checkpoint))
        self.weights = model_zoo.get_checkpoint_url(checkpoint)
        self.labels = COCO_LABELS
        self.confidence_threshold = confidence_threshold