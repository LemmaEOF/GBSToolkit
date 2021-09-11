from dataclasses import dataclass
from typing import Any, Dict

from .project import Project


@dataclass
class FormatContext:
    project: Project
    args: Dict[str, Any]
