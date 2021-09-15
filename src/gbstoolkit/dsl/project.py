from dataclasses import dataclass
from typing import Dict, List, Optional

from .assets import Background, SpriteSheet, Song
from .event import CustomEvent
from .marshalling import JsonSafe, serialize, Serializable
from .palette import Palette
from .scene import Scene
from .settings import Settings
from .util import NameUtil


class ProjectNameUtil(NameUtil):
    def __init__(self):
        self.id_to_background = {}
        self.background_to_id = {}
        self.id_to_scene = {}
        self.scene_to_id = {}
        self.id_to_song = {}
        self.song_to_id = {}
        self.id_to_sprite = {}
        self.sprite_to_id = {}

    def add_background(self, id: str, name: str):
        self.id_to_background[id] = name
        self.background_to_id[name] = id

    def add_scene(self, id: str, name: str):
        self.id_to_scene[id] = name
        self.scene_to_id[name] = id

    def add_song(self, id: str, name: str):
        self.id_to_song[id] = name
        self.song_to_id[name] = id

    def add_sprite(self, id: str, name: str):
        self.id_to_sprite[id] = name
        self.sprite_to_id[name] = id

    def actor_for_id(self, id: str) -> str:
        return NotImplemented

    def id_for_actor(self, name: str) -> str:
        return NotImplemented

    def background_for_id(self, id: str) -> str:
        return self.id_to_background[id]

    def id_for_background(self, name: str) -> str:
        return self.background_to_id[name]

    def scene_for_id(self, id: str) -> str:
        return self.id_to_scene[id]

    def id_for_scene(self, name: str) -> str:
        return self.scene_to_id[name]

    def song_for_id(self, id: str) -> str:
        return self.id_to_song[id]

    def id_for_song(self, name: str) -> str:
        return self.song_to_id[name]

    def sprite_for_id(self, id: str) -> str:
        return self.id_to_sprite[id]

    def id_for_sprite(self, name: str) -> str:
        return self.sprite_to_id[name]


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

    def format(self):  # TODO: return type(s)
        names = ProjectNameUtil()
        for background in self.backgrounds:
            names.add_background(str(background.id), background.name)
        for scene in self.scenes:
            names.add_scene(str(scene.id), scene.name)  # TODO: sanitize for safety!
        for song in self.music:
            names.add_song(str(song.id), song.name)
        for sprite in self.sprite_sheets:
            names.add_sprite(str(sprite.id), sprite.name)
        # TODO: rest of formatting here!

