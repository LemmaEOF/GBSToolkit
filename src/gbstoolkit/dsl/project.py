from dataclasses import dataclass
from typing import Dict, List, Optional

from .assets import Background, SpriteSheet, Song
from .event import CustomEvent
from .marshalling import JsonSafe, serialize, Serializable
from .palette import Palette
from .scene import Scene
from .settings import Settings


@dataclass
class Project(Serializable):
    name: str
    author: str
    version: str
    release: str
    notes: Optional[str]
    scenes: List[Scene]
    backgrounds: List[Background]
    sprite_sheets: List[SpriteSheet]
    palettes: List[Palette]
    custom_events: List[CustomEvent]
    music: List[Song]
    variables: Dict[str, str]
    settings: Settings

    def serialize(self) -> JsonSafe:
        ret = {
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
            "variables": [{"id": i[0], "name": i[1]} for i in self.variables.items()],
            "settings": serialize(self.settings)
        }
        if self.notes is not None:
            ret["notes"] = self.notes
        return ret

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Project":
        # this is just fine, PyTypeChecker doesn't think a value in obj is a JsonSafe
        # noinspection PyTypeChecker
        return Project(
            name=obj["name"],
            author=obj["author"],
            version=obj["_version"],
            release=obj["_release"],
            notes=obj["notes"] if "notes" in obj else None,
            scenes=[Scene.deserialize(i) for i in obj["scenes"]],
            backgrounds=[Background.deserialize(i) for i in obj["backgrounds"]],
            sprite_sheets=[SpriteSheet.deserialize(i) for i in obj["spriteSheets"]],
            palettes=[Palette.deserialize(i) for i in obj["palettes"]],
            custom_events=[CustomEvent.deserialize(i) for i in obj["customEvents"]],
            music=[Song.deserialize(i) for i in obj["music"]],
            variables={i["id"]: i["name"] for i in obj["variables"]},
            settings=Settings.deserialize(obj["settings"])
        )

