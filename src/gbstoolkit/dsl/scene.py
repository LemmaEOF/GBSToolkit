from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID

from .actor import Actor
from .enums import SceneType
from .event import Event
from .marshalling import JsonSafe, serialize, Serializable
from .palette import Palette
from .trigger import Trigger
from .util import NameUtil


class SceneNameUtil(NameUtil):
    def __init__(self, parent: NameUtil):
        self.parent = parent
        self.id_to_actor = {}
        self.actor_to_id = {}

    def add_actor(self, id: str, name: str):
        self.id_to_actor[id] = name
        self.actor_to_id[name] = id

    def actor_for_id(self, id: str) -> str:
        if id == "player" or id == "$self$" or id.isdecimal():
            return id
        return self.id_to_actor[id]

    def id_for_actor(self, name: str) -> str:
        if name == "player" or name == "$self$" or name.isdecimal():
            return name
        return self.actor_to_id[name]

    def background_for_id(self, id: str) -> str:
        return self.parent.background_for_id(id)

    def id_for_background(self, name: str) -> str:
        return self.parent.id_for_background(name)

    def scene_for_id(self, id: str) -> str:
        return self.parent.scene_for_id(id)

    def id_for_scene(self, name: str) -> str:
        return self.parent.id_for_scene(name)

    def song_for_id(self, id: str) -> str:
        return self.parent.song_for_id(id)

    def id_for_song(self, name: str) -> str:
        return self.parent.id_for_song(name)

    def sprite_for_id(self, id: str) -> str:
        return self.parent.sprite_for_id(id)

    def id_for_sprite(self, name: str) -> str:
        return self.parent.id_for_sprite(name)


@dataclass
class Scene(Serializable):
    id: UUID
    name: str
    type: SceneType
    background_id: UUID
    palette_ids: List[Optional[UUID]]
    x: float
    y: float
    width: int
    height: int
    notes: Optional[str]
    label_color: Optional[str]
    actors: List[Actor]
    triggers: List[Trigger]
    collisions: List[int]  # TODO: better format for parsed then compile down to the flat one?
    tile_colors: List[int]
    script: List[Event]
    player_hit1_script: List[Event]
    player_hit2_script: List[Event]
    player_hit3_script: List[Event]

    def serialize(self) -> JsonSafe:
        ret = {
            "id": serialize(self.id),
            "name": self.name,
            "type": serialize(self.type),
            "backgroundId": self.background_id,
            "paletteIds": self.palette_ids,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "actors": serialize(self.actors),
            "triggers": serialize(self.triggers),
            "collisions": self.collisions,
            "tileColors": self.tile_colors,
            "script": serialize(self.script),
            "playerHit1Script": serialize(self.player_hit1_script),
            "playerHit2Script": serialize(self.player_hit2_script),
            "playerHit3Script": serialize(self.player_hit3_script)
        }
        if self.notes is not None:
            ret["notes"] = self.notes
        if self.label_color is not None:
            ret["labelColor"] = self.label_color
        return ret

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Scene":
        return Scene(
            id=UUID(obj["id"]),
            name=obj["name"],
            type=SceneType.deserialize(obj["type"]) if "type" in obj else "0",
            background_id=UUID(obj["id"]),
            palette_ids=[Palette.parse_id(i) for i in obj["paletteIds"]] if "paletteIds" in obj else [],
            x=obj["x"],
            y=obj["y"],
            width=obj["width"],
            height=obj["height"],
            notes=obj["notes"] if "notes" in obj else None,
            label_color=obj["labelColor"] if "labelColor" in obj else None,
            actors=[Actor.deserialize(i) for i in obj["actors"]],
            triggers=[Trigger.deserialize(i) for i in obj["triggers"]],
            collisions=obj["collisions"],
            tile_colors=obj["tileColors"] if "tileColors" in obj else [],
            script=[Event.deserialize(i) for i in obj["script"]],
            player_hit1_script=[Event.deserialize(i) for i in obj["playerHit1Script"]],
            player_hit2_script=[Event.deserialize(i) for i in obj["playerHit2Script"]],
            player_hit3_script=[Event.deserialize(i) for i in obj["playerHit3Script"]]
        )
