#!/usr/bin/env python
from pathlib import Path
from collections import defaultdict
from typing import Union
import json
import requests

from pythiags import Consumer

from safe_common.dates import now
from safe_common.envs import API_CRUD_ENDPOINT
from safe_common.logger import get_logger

from app.utils.events import check_detection_importance
from app.utils.events import cast_detection
from app.utils.events import cast_frame
from app.utils.events import SELECTED_ROIS
from app.utils.utils import traced


logger = get_logger(__name__)


class DDBBWriter(Consumer):
    def __init__(
        self,
    ):
        self.video_recorder = None
        self.selected_rois = SELECTED_ROIS
        self.current_event = {}  # TODO: Implement lock to avoid read/write clash.
        self.frames = defaultdict(
            list
        )  # TODO: Implement lock to avoid read/write clash.

    @traced(logger.info)
    def create_event(
        self, event_type: str, evidence_video_path: Path, source_id: int
    ) -> int:
        event_metadata = dict(
            timestamp=now(as_string=True),  # TODO: Get timestamp closer to source
            event_type=event_type,
            evidence_video_path=str(evidence_video_path),
            camera_id=int(source_id) + 1,  # TODO: Check if source_id==camera_id
        )
        create_event_response = requests.post(
            f"https://{API_CRUD_ENDPOINT}/events/",
            json=event_metadata,
            verify=False,
        )
        if create_event_response.ok:
            event_id = create_event_response.json()["event_id"]
            return event_id

    def dump_metadata(self, meta: dict):
        for (source_id, frame_number), full_metadata in meta.items():
            frame_metadata = full_metadata["analytics"]
            detection_metadata = full_metadata["detections"]
            important_detections = self.filter_detections(detection_metadata)

            if not len(important_detections):
                continue

            logger.warning(f"Detected event on camera {source_id+1}")
            evidence_video_path = self.video_recorder.record(
                source_id
            )  # FIXME where is the on_video_finished hook to upload recorded videos?

            if source_id not in self.current_event:
                logger.info(f"Creating new event on camera {source_id+1}")
                try:
                    event_id = self.create_event(
                        evidence_video_path=evidence_video_path,
                        source_id=source_id,
                        event_type="Trespassing",
                    )
                    self.current_event[source_id] = (event_id, evidence_video_path)
                    logger.info("Event created succesfully.")
                except Exception as exc:
                    logger.error(f"Could not create event. Error: {exc}")
                    continue
            else:
                (event_id, evidence_video_path) = self.current_event[source_id]
                logger.info(f"Appending to event {event_id} on camera {source_id+1}")

            registered_detections = []
            for detection in important_detections:
                rois = []
                for obj in detection["objects"]:
                    rois.extend(obj["roiStatus"])
                registered_detection = cast_detection(detection, rois, event_id)
                registered_detections.append(registered_detection)

            registered_frame = cast_frame(
                frame_metadata,
                source_id,
                frame_number,
                registered_detections,
            )
            self.frames[source_id].append(
                registered_frame
            )  # Check wether we should upload this or detections

    def _on_video_finished(self, video_path: Union[str, Path]):
        """Upload event detections and cleanup."""
        sources = {
            video_path: source for source, (_, video_path) in self.current_event.items()
        }
        corresponding_source_id = sources[video_path]

        # Video is finished, so it has to be removed from current events
        event_id, video_path = self.current_event.pop(corresponding_source_id)

        # Retrieve finished events detections...
        event_frames = self.frames.pop(corresponding_source_id)
        logger.info(
            f"Found {len(event_frames)} for event {event_id}. Uploading to DB..."
        )

        print(f"FRAMES DETAIL: {event_frames}")

        if event_frames:
            upload_frames_response = requests.post(
                f"https://{API_CRUD_ENDPOINT}/events/{event_id}/frames",
                json=event_frames,
                verify=False,
            )
            if upload_frames_response.ok:
                logger.info(f"Uploading detections for event {event_id}...")
            else:
                logger.error(
                    f"Could not upload detections for event {event_id} ({upload_frames_response.status_code}): {upload_frames_response.text} ..."
                )

    def filter_detections(self, detections: list) -> list:
        return [
            detection
            for detection in detections
            if check_detection_importance(detection, self.selected_rois)
        ]

    def incoming(self, events):
        self.dump_metadata(events)

    def set_video_recorder(self, multi_video_recorder):
        self.video_recorder = multi_video_recorder
        for (
            _,
            recorder,
        ) in self.video_recorder.recorders.items():  # Append observer to each recorder
            recorder.add_observer(self)
