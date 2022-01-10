from fastapi import APIRouter
from schema.annotations import InstanceSegmentationAnnotationList
from schema.requests import LabelRequest
# from schema.images import RawImageList
# from schema.images import MaskAnnotatedImageList
# from schema.images import BboxAnnotatedImageList
# from schema.models import SegmentationModel
# from schema.models import ObjectDetectionModel


router = APIRouter(
    tags=["label"],
    responses={404: {"description": "Not found"}},
)


@router.post("/mask", response_model = InstanceSegmentationAnnotationList)
async def get_mask_labels(task_params: LabelRequest) -> InstanceSegmentationAnnotationList:
    """Retrieve masks from the provided images, using an image segmentation model."""
    from create_dataset.backend.detectron.inference import InferenceModel
    model = InferenceModel(task_params.model_name)
    results = model.run_inference(task_params.video_path)
    print(f"Sample result: {results[0]}")
    return results
    # from app.utils.inference import SegmentationModel
    # model = SegmentationModel(
    #     model_file = model.file, 
    #     confidence_threshold = model.confidence_threshold,
    #     iou_threshold = model.iou_threshold
    # )
    # image_paths = [image.path for image in images.__root__]
    # mask_annotations = model.run_inference(images = image_paths)
    # return mask_annotations


# @router.post("/bbox")
# async def get_bbox_labels(model: ObjectDetectionModel, images:RawImageList) -> BboxAnnotatedImageList:
#     """Retrieve bounding boxes from the provided images, using an object detection model."""
#     raise NotImplementedError
    # from app.utils.inference import ObjectDetectionModel
    # model = ObjectDetectionModel(
    #     model_file = model.file, 
    #     confidence_threshold = model.confidence_threshold,
    #     iou_threshold = model.iou_threshold
    # )
    # image_paths = [image.path for image in images.__root__]
    # bbox_annotations = model.run_inference(images = image_paths)
    # return bbox_annotations
