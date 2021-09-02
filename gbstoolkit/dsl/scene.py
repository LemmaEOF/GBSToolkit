from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID

from actor import Actor
from enums import SceneType
from event import Event
from marshalling import JsonSafe, serialize, Serializable
from trigger import Trigger


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
    triggers: List[Trigger]
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
            "triggers": serialize(self.triggers),
            "collisions": self.collisions,
            "tileColors": self.tile_colors,
            "script": serialize(self.script),
            "playerHit1Script": serialize(self.player_hit1_script),
            "playerHit2Script": serialize(self.player_hit2_script),
            "playerHit3Script": serialize(self.player_hit3_script)
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Scene":
        id = UUID(obj["id"])
        name = obj["name"]
        type = SceneType.deserialize(obj["type"])
        background_id = UUID(obj["id"])
        palette_ids = [UUID(i) if i is not None else None for i in obj["paletteIds"]]
        x = obj["x"]
        y = obj["y"]
        width = obj["width"]
        height = obj["height"]
        actors = [Actor.deserialize(i) for i in obj["actors"]]
        triggers = [Trigger.deserialize(i) for i in obj["triggers"]]
        collisions = obj["collisions"]
        tile_colors = obj["tileColors"]
        script = [Event.deserialize(i) for i in obj["script"]]
        player_hit1_script = [Event.deserialize(i) for i in obj["playerHit1Script"]]
        player_hit2_script = [Event.deserialize(i) for i in obj["playerHit2Script"]]
        player_hit3_script = [Event.deserialize(i) for i in obj["playerHit3Script"]]
        return Scene(id=id, name=name, type=type, background_id=background_id, palette_ids=palette_ids, x=x, y=y,
                     width=width, height=height, actors=actors, triggers=triggers, collisions=collisions,
                     tile_colors=tile_colors, script=script, player_hit1_script=player_hit1_script,
                     player_hit2_script=player_hit2_script, player_hit3_script=player_hit3_script)
