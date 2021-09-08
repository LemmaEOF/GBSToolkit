from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID

from .enums import Direction, MovementType, SpriteType
from .event import Event
from .marshalling import JsonSafe, serialize, Serializable


@dataclass
class Actor(Serializable):
    id: UUID
    name: str
    sprite_sheet_id: UUID
    sprite_type: SpriteType
    x: int
    y: int
    movement_type: MovementType
    direction: Direction
    move_speed: int
    anim_speed: int
    collision_group: str
    notes: Optional[str]
    script: List[Event]
    start_script: List[Event]
    update_script: List[Event]
    hit1_script: List[Event]
    hit2_script: List[Event]
    hit3_script: List[Event]

    def serialize(self) -> JsonSafe:
        ret = {
            "id": serialize(self.id),
            "name": self.name,
            "spriteSheetId": serialize(self.sprite_sheet_id),
            "spriteType": serialize(self.sprite_type),
            "x": self.x,
            "y": self.y,
            "movementType": serialize(self.movement_type),
            "direction": serialize(self.direction),
            "moveSpeed": self.move_speed,
            "animSpeed": self.anim_speed,
            "collisionGroup": self.collision_group,
            "script": serialize(self.script),
            "startScript": serialize(self.start_script),
            "updateScript": serialize(self.update_script),
            "hit1Script": serialize(self.hit1_script),
            "hit2Script": serialize(self.hit2_script),
            "hit3Script": serialize(self.hit3_script)
        }
        if self.notes is not None:
            ret["notes"] = self.notes
        return ret

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Actor":
        return Actor(
            id=UUID(obj["id"]),
            name=obj["name"] if "name" in obj else "",
            sprite_sheet_id=UUID(obj["id"]),
            sprite_type=SpriteType.deserialize(obj["spriteType"]),
            x=obj["x"],
            y=obj["y"],
            movement_type=MovementType.deserialize(obj["movementType"])
            if "movementType" in obj else MovementType.STATIC,
            direction=Direction.deserialize(obj["direction"]),
            move_speed=obj["move_speed"] if "move_speed" in obj else 3,
            anim_speed=obj["anim_speed"] if "move_speed" in obj else 3,
            collision_group=obj["collisionGroup"],
            notes=obj["notes"] if "notes" in obj else None,
            script=[Event.deserialize(i) for i in obj["script"]] if "script" in obj else [],
            start_script=[Event.deserialize(i) for i in obj["startScript"]] if "startScript" in obj else [],
            update_script=[Event.deserialize(i) for i in obj["updateScript"]] if "updateScript" in obj else [],
            hit1_script=[Event.deserialize(i) for i in obj["hit1Script"]] if "hit1Script" in obj else [],
            hit2_script=[Event.deserialize(i) for i in obj["hit2Script"]] if "hit2Script" in obj else [],
            hit3_script=[Event.deserialize(i) for i in obj["hit3Script"]] if "hit3Script" in obj else []
        )
