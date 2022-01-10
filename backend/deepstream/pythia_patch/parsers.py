from typing import Union

import pyds
import pyds_bbox_meta
import pyds_tracker_meta

from pythiags.models import Bbox


def _bounding_box(coords: pyds.NvOSD_RectParams) -> Bbox:
    return Bbox(
        int(coords.left),
        int(coords.top),
        int(coords.left + coords.width),
        int(coords.top + coords.height),
    )


def detector_bbox(obj_meta: pyds_bbox_meta.NvDsObjectMeta) -> Bbox:
    """Detector Bounding box from NvDsObjectMeta."""
    return _bounding_box(obj_meta.detector_bbox_info.org_bbox_coords)


def instance_segmentation_mask(obj_meta: )