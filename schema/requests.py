from typing import Optional

from pydantic import BaseModel

class LabelRequest(BaseModel):
    model_name: Optional[str]
    video_path: str