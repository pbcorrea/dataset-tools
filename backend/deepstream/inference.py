#1. Create Pythia Standalone
#2. Load model
#3. Create nvinfer.conf
#4. Verify images are correct 
#5. Run inference
#6. Parse incoming annotations 
#7. Return labels


import os
from pathlib import Path
import sys
from time import sleep
from logging import getLogger

import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

from pythiags.headless import Standalone

from app.utils.utils import get_by_name_or_raise
from app.utils.utils import pipe_from_file

from app.utils.extractor import ObjectDetectionExtractor
from app.utils.extractor import InstanceSegmentationExtractor
from app.utils.consumer import DDBBWriter

logger = getLogger()


def await_pipeline(timeout_sec=10):
    # # TODO: this must be performed after application runs because we need application.cameras
    # maybe we could use a gsttreamer probe instead
    t0 = now()
    while True:
        if (now() - t0).total_seconds() > timeout_sec:
            raise TimeoutError(f"Unable to get pipeline status. state={state}")
        state_change_return, current, pending = state = application.pipeline.get_state(
            1
        )
        if state_change_return == Gst.StateChangeReturn.SUCCESS:
            return True
        if state_change_return == Gst.StateChangeReturn.ASYNC:
            sleep(0.5)
            continue
        if current != Gst.State.PLAYING:
            raise ValueError(f"Unable to play pipeline. state={state}")


class InferenceModel(Standalone):
    def __init__(self, pipeline: str, mode: str, *a, **kw):
        self._producer = ObjectDetectionExtractor() if mode == "detection" else InstanceSegmentationExtractor()
        self._consumer = DDBBWriter()
        kw.setdefault(
            "metadata_extraction_map",
            {
                "analytics": (self._producer, self._consumer),
            },
        )
        super().__init__(pipeline_str, *a, **kw)

    
    def __call__(self, *a, **kw):
        super().__call__(*a, **kw)
    
    @property
    def demux(self):
        return get_by_name_or_raise(self.pipeline, "demux")

    @property
    def muxer(self):
        return get_by_name_or_raise(self.pipeline, "nvmuxer")

    @property
    def tiler(self):
        return get_by_name_or_raise(self.pipeline, "tiler")

    def on_eos(self, bus, message):
        logger.info("Gstreamer: End-of-stream")
        self.join()

    def on_error(self, bus, message):
        err, debug = message.parse_error()
        logger.error("Gstreamer: %s: %s" % (err, debug))

pipeline_str = pipe_from_file(
    "app/pipeline.gstp.jinja",
    cameras=CAMERAS,
    multistreamtiler_width=MULTISTREAMTILER_WIDTH,
    multistreamtiler_height=MULTISTREAMTILER_HEIGHT,
    analytics_config_file=ANALYTICS_CONFIGURATION_FILE,
    pgie_config_file=PGIE_CONFIG_FILE,
    tracker_config_file=TRACKER_CONFIG_FILE,
)
logger.debug(pipeline_str)

application = InferenceModel(pipeline_str)
