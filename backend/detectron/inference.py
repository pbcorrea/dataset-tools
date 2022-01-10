from typing import List
from time import perf_counter
from logging import getLogger

from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor

from create_dataset.backend.detectron.models import MaskRCNN
from create_dataset.utils.video import Video


logger = getLogger(__name__)

class InferenceModel:
    def __init__(self, model_name: str="mask_rcnn") -> None:
        self.config = get_cfg()
        self.model = MaskRCNN()
        
    def setup(self,):    
        self.config.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.self.model.confidence_threshold
        self.config.merge_from_file(self.model.config)


    def run_inference(self, video_path: str) -> List[dict]:
        """Retrieve annnotated images from video."""
        predictor = DefaultPredictor(self.config)
        inference_results = []
        video = Video(video_path)
        inference_start = perf_counter()
        for image in video.get_images():
            inference_results.append(predictor(image))
        logger.info(f"Processed {len(inference_results)} in {(perf_counter()-inference_start):.3f} seconds")
        return inference_results