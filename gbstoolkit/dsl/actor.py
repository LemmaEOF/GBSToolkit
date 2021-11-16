from dataclasses import dataclass
from typing import Dict, List, Optional
import uuid
from uuid import UUID

from kdl import Document

from .enums import Direction, AutoMovementType, SpriteType
from .event import Event
from .marshalling import JsonSafe, serialize, Serializable
from .util import NameUtil, ProgressTracker, prop_node, map_nodes


@dataclass
class Actor(Serializable):
    id: UUID
    name: str
    sprite_sheet_id: UUID
    sprite_type: SpriteType
    frame: int
    x: int
    y: int
    movement_type: AutoMovementType
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
    scene_index: int

    def serialize(self) -> JsonSafe:
        ret = {
            "id": serialize(self.id),
            "spriteSheetId": serialize(self.sprite_sheet_id),
            "x": self.x,
            "y": self.y,
            "movementType": serialize(self.movement_type),
            "direction": serialize(self.direction),
            "script": serialize(self.script),
            "moveSpeed": self.move_speed,
            "frame": self.frame,
            "spriteType": serialize(self.sprite_type),
            "updateScript": serialize(self.update_script),
            "startScript": serialize(self.start_script),
            "hit1Script": serialize(self.hit1_script),
            "hit2Script": serialize(self.hit2_script),
            "hit3Script": serialize(self.hit3_script),
            "name": self.name,
            "animSpeed": self.anim_speed,
            "collisionGroup": self.collision_group
        }
        if self.notes is not None:
            ret["notes"] = self.notes
        return ret

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe], scene_index: int) -> "Actor":
        return Actor(
            id=UUID(obj["id"]),
            name=obj["name"] if "name" in obj else "",
            sprite_sheet_id=UUID(obj["spriteSheetId"]),
            sprite_type=SpriteType.deserialize(obj["spriteType"]),
            frame=obj["frame"] if "frame" in obj else 0,
            x=obj["x"],
            y=obj["y"],
            movement_type=AutoMovementType.deserialize(obj["movementType"])
            if "movementType" in obj else AutoMovementType.STATIC,
            direction=Direction.deserialize(obj["direction"]),
            move_speed=obj["moveSpeed"] if "moveSpeed" in obj else 3,
            anim_speed=obj["animSpeed"] if "animSpeed" in obj else 3,
            collision_group=obj["collisionGroup"],
            notes=obj["notes"] if "notes" in obj else None,
            script=[Event.deserialize(i) for i in obj["script"]] if "script" in obj else [],
            start_script=[Event.deserialize(i) for i in obj["startScript"]] if "startScript" in obj else [],
            update_script=[Event.deserialize(i) for i in obj["updateScript"]] if "updateScript" in obj else [],
            hit1_script=[Event.deserialize(i) for i in obj["hit1Script"]] if "hit1Script" in obj else [],
            hit2_script=[Event.deserialize(i) for i in obj["hit2Script"]] if "hit2Script" in obj else [],
            hit3_script=[Event.deserialize(i) for i in obj["hit3Script"]] if "hit3Script" in obj else [],
            scene_index=scene_index
        )

    def format(self, names: NameUtil) -> Dict[str, Document]:
        meta = Document()
        meta.nodes.extend([
            prop_node("id", self.id),
            prop_node("name", self.name),
            prop_node("spriteSheet", names.sprite_for_id(serialize(self.sprite_sheet_id))),
            prop_node("spriteType", self.sprite_type.serialize()),
            prop_node("startFrame", self.frame),
            prop_node("x", self.x),
            prop_node("y", self.y),
            prop_node("movementType", self.movement_type.serialize()),
            prop_node("direction", self.direction),
            prop_node("moveSpeed", self.move_speed),
            prop_node("animSpeed", self.anim_speed),
            prop_node("collisionGroup", self.collision_group),
            prop_node("__index", self.scene_index)
        ])
        if self.notes is not None:
            meta.nodes.append(prop_node("notes", self.notes))
        docs = {"meta": meta}
        if len(self.script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, names) for i in self.script])
            docs["interact"] = script
        if len(self.start_script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, names) for i in self.start_script])
            docs["init"] = script
        if len(self.update_script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, names) for i in self.update_script])
            docs["update"] = script
        if len(self.hit1_script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, names) for i in self.hit1_script])
            docs["hit-1"] = script
        if len(self.hit2_script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, names) for i in self.hit2_script])
            docs["hit-2"] = script
        if len(self.hit3_script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, names) for i in self.hit3_script])
            docs["hit-3"] = script
        return docs

    @staticmethod
    def parse(docs: Dict[str, Document], names: NameUtil, progress: ProgressTracker) -> "Actor":
        meta = docs["meta"]
        contents = map_nodes(meta.nodes)
        interact = [Event.parse(i, names, progress) for i in docs["interact"].nodes] if "interact" in docs else []
        init = [Event.parse(i, names, progress) for i in docs["init"].nodes] if "init" in docs else []
        update = [Event.parse(i, names, progress) for i in docs["update"].nodes] if "update" in docs else []
        hit_1 = [Event.parse(i, names, progress) for i in docs["hit-1"].nodes] if "hit-1" in docs else []
        hit_2 = [Event.parse(i, names, progress) for i in docs["hit-2"].nodes] if "hit-2" in docs else []
        hit_3 = [Event.parse(i, names, progress) for i in docs["hit-3"].nodes] if "hit-3" in docs else []
        return Actor(
            id=UUID(contents["id"]) if "id" in contents else uuid.uuid4(),
            name=contents["name"] if "name" in contents else "",
            sprite_sheet_id=UUID(names.id_for_sprite(contents["spriteSheet"])),
            sprite_type=SpriteType.deserialize(contents["spriteType"]),
            frame=contents["startFrame"],
            x=contents["x"],
            y=contents["y"],
            movement_type=AutoMovementType.deserialize(contents["movementType"])
            if "movementType" in contents else AutoMovementType.STATIC,
            direction=Direction.deserialize(contents["direction"]),
            move_speed=contents["moveSpeed"] if "moveSpeed" in contents else 3,
            anim_speed=contents["animSpeed"] if "moveSpeed" in contents else 3,
            collision_group=contents["collisionGroup"],
            notes=contents["notes"] if "notes" in contents else None,
            script=interact,
            start_script=init,
            update_script=update,
            hit1_script=hit_1,
            hit2_script=hit_2,
            hit3_script=hit_3,
            scene_index=int(contents["__index"])
        )
