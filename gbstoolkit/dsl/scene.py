from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from actor import Actor
from enums import SceneType
from event import Event
from marshalling import JsonSafe, serialize, Serializable


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
    actors: List[Actor]
    collisions: List[int]  # TODO: better format for parsed then compile down to the flat one?
    tile_colors: List[int]
    script: List[Event]
    player_hit1_script: List[Event]
    player_hit2_script: List[Event]
    player_hit3_script: List[Event]

    def serialize(self) -> JsonSafe:
        return {
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
            "collisions": self.collisions,
            "tileColors": self.tile_colors,
            "script": serialize(self.script),
            "playerHit1Script": serialize(self.player_hit1_script),
            "playerHit2Script": serialize(self.player_hit2_script),
            "playerHit3Script": serialize(self.player_hit3_script)
        }
