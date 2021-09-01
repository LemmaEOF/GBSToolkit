from dataclasses import dataclass
from typing import List

from assets import Background, SpriteSheet, Song
from event import CustomEvent
from marshalling import JsonSafe, serialize, Serializable, Variable
from palette import Palette
from scene import Scene
from settings import Settings


@dataclass
class Project(Serializable):
    name: str
    author: str
    version: str
    release: str
    scenes: List[Scene]
    backgrounds: List[Background]
    sprite_sheets: List[SpriteSheet]
    palettes: List[Palette]
    custom_events: List[CustomEvent]
    music: List[Song]
    variables: List[Variable]
    settings: List[Settings]

    def serialize(self) -> JsonSafe:
        return {
            "name": self.name,
            "author": self.author,
            "_version": self.version,
            "_release": self.release,
            "scenes": serialize(self.scenes),
            "backgrounds": serialize(self.backgrounds),
            "spriteSheets": serialize(self.sprite_sheets),
            "palettes": serialize(self.palettes),
            "customEvents": serialize(self.custom_events),
            "music": serialize(self.music),
            "variables": serialize(self.variables),
            "settings": serialize(self.settings)
        }