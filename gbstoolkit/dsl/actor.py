from dataclasses import dataclass
from typing import Dict, List
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

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Actor":
        id = UUID(obj["id"])
        name = obj["name"]
        sprite_sheet_id = UUID(obj["id"])
        sprite_type = SpriteType.deserialize(obj["spriteType"])
        x = obj["x"]
        y = obj["y"]
        movement_type = MovementType.deserialize(obj["movementType"])
        direction = Direction.deserialize(obj["direction"])
        move_speed = obj["move_speed"]
        anim_speed = obj["anim_speed"]
        collision_group = obj["collisionGroup"]
        script = [Event.deserialize(i) for i in obj["script"]]
        start_script = [Event.deserialize(i) for i in obj["startScript"]]
        update_script = [Event.deserialize(i) for i in obj["updateScript"]]
        hit1_script = [Event.deserialize(i) for i in obj["hit1Script"]]
        hit2_script = [Event.deserialize(i) for i in obj["hit2Script"]]
        hit3_script = [Event.deserialize(i) for i in obj["hit3Script"]]
        return Actor(id=id, name=name, sprite_sheet_id=sprite_sheet_id, sprite_type=sprite_type, x=x, y=y, movement_type=movement_type,
                     direction=direction, move_speed=move_speed, anim_speed=anim_speed, collision_group=collision_group,
                     script=script, start_script=start_script, update_script=update_script, hit1_script=hit1_script,
                     hit2_script=hit2_script, hit3_script=hit3_script)
