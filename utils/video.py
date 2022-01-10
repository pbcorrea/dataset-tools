from pathlib import Path

import cv2


class Video:
    def __init__(self, video_path: Path)-> None:
        self.video_capture = self.setup(Path(video_path).resolve())


    def setup(self, video_path:Path):
        """Check that a valid video exists at the specified location."""
        if not video_path.exists():
            raise RuntimeError(f"No video file found at {video_path}.")
        if not video_path.stat().st_size > 0:
            raise RuntimeError(f"Video file at {video_path} is empty.")
        self.capture = cv2.VideoCapture(str(video_path))
        ret, frame = self.capture.read()
        if not ret:
            raise ValueError(f"Could not read frames from video at {video_path}")


    def get_images(self, ):
        """Yield images from loaded video."""
        images_remaining = True
        while images_remaining:
            ret, frame = self.capture.read()
            if not ret:
                images_remaining = False
            yield frame
    