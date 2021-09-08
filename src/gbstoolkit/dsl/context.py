from dataclasses import dataclass

from .project import Project


@dataclass
class CommandContext:
    project: Project
