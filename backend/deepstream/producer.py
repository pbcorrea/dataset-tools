#!/usr/bin/env python

from pythiags import frames_per_batch
from pythiags import objects_per_frame
from pythiags import Producer
from pythiags.deepstream.iterators import analytics_per_frame
from pythiags.deepstream.iterators import analytics_per_object
from pythiags.deepstream.parsers import last_bbox as detector_bbox


class MetadataExtractor(Producer):
    def extract_metadata(self, pad, info):
        meta = {}
        for frame_metadata in frames_per_batch(info):
            parsed_metadata = self.parse(frame_metadata)
            if not parsed_metadata:
                continue

            meta[frame_metadata.frame_num] = {
                "detections": parsed_metadata,
            }
        return meta


class ObjectDetectionExtractor(MetadataExtractor):
    @classmethod
    def parse(cls, frame_metadata):
        return [
            {
                "tracked_object_id": obj_meta.object_id,
                "label": obj_meta.obj_label,
                "confidence": obj_meta.confidence,
                "frame_number": frame_metadata.frame_num,
                "bbox": detector_bbox(obj_meta),
                "objects": cls.parse_object_analytics(frame_metadata, obj_meta),
            }
            for obj_meta in objects_per_frame(frame_metadata)
        ]


class InstanceSegmentationExtractor(MetadataExtractor):
    @classmethod
    def parse(cls, frame_metadata):
        return [
            {
                "tracked_object_id": obj_meta.object_id,
                "label": obj_meta.obj_label,
                "confidence": obj_meta.confidence,
                "frame_number": frame_metadata.frame_num,
                "bbox": detector_bbox(obj_meta),
                "objects": cls.parse_object_analytics(frame_metadata, obj_meta),
            }
            for obj_meta in objects_per_frame(frame_metadata)
        ]


class SemanticSegmentationExtractor(MetadataExtractor):
    @classmethod
    def parse(cls, frame_metadata):
        raise NotImplementedError(f"Semantic segmentation has not been implemented yet.")


class ActionRecognitionExtractor(MetadataExtractor):
    @classmethod
    def parse(cls, frame_metadata):
        raise NotImplementedError(f"Semantic segmentation has not been implemented yet.")

