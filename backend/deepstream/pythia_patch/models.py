"""Model definitions."""

from typing import List
from typing import NamedTuple
from typing import Tuple


Vertex = Tuple[float]

class Mask(NamedTuple):
    """Polygonal mask used for instance segmentation."""
    vertices: List[Vertex]