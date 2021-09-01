from dataclasses import dataclass
from typing import List
from uuid import UUID

from enums import Direction, MovementType, SpriteType
from event import Event
from marshalling import JsonSafe, serialize, Serializable


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
    script: List[Event]
    start_script: List[Event]
    update_script: List[Event]
    hit1_script: List[Event]
    hit2_script: List[Event]
    hit3_script: List[Event]

    def serialize(self) -> JsonSafe:
        return {
            "id": serialize(self.id),
            "name": self.name,
            "spriteSheetId": serialize(self.sprite_sheet_id),
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

