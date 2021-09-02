from dataclasses import dataclass
from typing import Dict, List

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
    settings: Settings

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

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Project":
        name = obj["name"]
        author = obj["author"]
        version = obj["_version"]
        release = obj["_release"]
        scenes = [Scene.deserialize(i) for i in obj["scenes"]]
        backgrounds = [Background.deserialize(i) for i in obj["backgrounds"]]
        sprite_sheets = [SpriteSheet.deserialize(i) for i in obj["spriteSheets"]]
        palettes = [Palette.deserialize(i) for i in obj["palettes"]]
        custom_events = [CustomEvent.deserialize(i) for i in obj["customEvents"]]
        music = [Song.deserialize(i) for i in obj["music"]]
        variables = [Variable.deserialize(i) for it in obj["variables"]]
        settings = Settings.deserialize(obj["settings"])
        return Project(name=name, author=author, version=version, release=release, scenes=scenes,
                       backgrounds=backgrounds, sprite_sheets=sprite_sheets, palettes=palettes,
                       custom_events=custom_events, music=music, variables=variables, settings=settings)