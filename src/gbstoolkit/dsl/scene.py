from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from kdl import Document, Node

from .actor import Actor
from .enums import SceneType
from .event import Event
from .marshalling import JsonSafe, serialize, Serializable
from .palette import Palette, PaletteID
from .trigger import Trigger
from .util import NameUtil, prop_node, sanitize_name


class SceneNameUtil(NameUtil):
    def __init__(self, parent: NameUtil):
        self.parent = parent
        self.id_to_actor = {}
        self.actor_to_id = {}
        self.id_to_trigger = {}
        self.trigger_to_id = {}
        self.actor_name_counts = {}
        self.trigger_name_counts = {}

    def add_actor(self, id: str, name: str):
        if name == "player" or name == "$self$" or name.isdecimal():
            print("Actor name '" + name + "' may overlap with built-in names! Renaming to '" + name + "-'!")
            name += "-"
        if name in self.actor_name_counts:
            print("Actor name '" + name + "' Already exists in this scene! Renaming to '" + name + "-"
                  + str(self.actor_name_counts[name] + 1) + "'!")
            self.actor_name_counts[name] += 1
            name += "-" + str(self.actor_name_counts[name])
        else:
            self.actor_name_counts[name] = 1
        self.id_to_actor[id] = name
        self.actor_to_id[name] = id

    def add_trigger(self, id: str, name: str):
        if name in self.trigger_name_counts:
            print("Trigger name '" + name + "' Already exists in this scene! Renaming to '" + name + "-'!"
                  + str(self.trigger_name_counts[name] + 1))
            self.trigger_name_counts[name] += 1
            name += "-" + str(self.trigger_name_counts[name])
        else:
            self.trigger_name_counts[name] = 1
        self.id_to_trigger[id] = name
        self.trigger_to_id[name] = id

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

    def custom_event_for_id(self, id: str) -> str:
        return self.parent.custom_event_for_id(id)

    def id_for_custom_event(self, name: str) -> str:
        return self.parent.id_for_custom_event(name)

    def palette_for_id(self, id: str) -> str:
        return self.parent.palette_for_id(id)

    def id_for_palette(self, name: str) -> str:
        return self.parent.id_for_palette(name)

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

    def trigger_for_id(self, id: str) -> str:
        return self.id_to_trigger[id]

    def id_for_trigger(self, name: str) -> str:
        return self.trigger_to_id[name]


@dataclass
class Scene(Serializable):
    id: UUID
    name: str
    type: SceneType
    background_id: UUID
    palette_ids: List[Optional[PaletteID]]
    x: float
    y: float
    width: int
    height: int
    notes: Optional[str]
    label_color: Optional[str]
    actors: List[Actor]
    triggers: List[Trigger]
    collisions: List[int]
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
            type=SceneType.deserialize(obj["type"]) if "type" in obj else SceneType.TOP_DOWN,
            background_id=UUID(obj["backgroundId"]),
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

    def format(self, names: NameUtil) -> Tuple[Dict[str, Document], NameUtil]:
        scene_names = SceneNameUtil(names)
        for actor in self.actors:
            if actor.name == "":
                scene_names.add_actor(str(actor.id), "actor-" + str(self.actors.index(actor)))
            else:
                scene_names.add_actor(
                    str(actor.id),
                    sanitize_name(actor.name, names.scene_for_id(str(self.id)) + " actor")
                )
        for trigger in self.triggers:
            if trigger.name == "":
                scene_names.add_trigger(str(trigger.id), "trigger-" + str(self.triggers.index(trigger)))
            else:
                scene_names.add_actor(
                    str(trigger.id),
                    sanitize_name(trigger.name, names.scene_for_id(str(self.id)) + " trigger")
                )
        meta = Document(preserve_property_order=True)
        meta.extend([
            prop_node("id", serialize(self.id)),
            prop_node("name", self.name),
            prop_node("type", self.type.serialize()),
            prop_node("background", scene_names.background_for_id(serialize(self.background_id))),
            prop_node("x", self.x),
            prop_node("y", self.y),
            prop_node("width", self.width),
            prop_node("height", self.height)
        ])
        if len(self.palette_ids) > 0:
            meta.append(Node(
                "palettes",
                None,
                None,
                [Node(
                    "palette" + str(self.palette_ids.index(i)),
                    None,
                    [names.palette_for_id(serialize(i))],
                    None
                ) for i in self.palette_ids if i is not None]
            ))
        if self.notes is not None:
            meta.append(prop_node("notes", self.notes))
        if self.label_color is not None:
            meta.append(prop_node("labelColor", self.label_color))
        docs = {"meta": meta}
        collisions = Document(preserve_property_order=True)
        tile_colors = Document(preserve_property_order=True)
        hasCollisions = len(self.collisions) > 0
        hasPalettes = len(self.tile_colors) > 0
        for y in range(self.height):
            for x in range(self.width):
                index = (self.width * y) + x
                if hasCollisions:
                    if index > len(self.collisions) - 1:
                        print("Tried to access index " + str(index) + " of collision list " + str(len(self.collisions))
                              + " long in scene `" + self.name + "` ! This shouldn't be possible!")
                        break
                    collision = self.collisions[index]
                    if collision & 0xF == 0xF:
                        collisions.append(Node("all", None, [x, y], None))
                    elif collision > 0:
                        if collision & 0x1 > 0:
                            collisions.append(Node("up", None, [x, y], None))
                        elif collision & 0x2 > 0:
                            collisions.append(Node("down", None, [x, y], None))
                        elif collision & 0x4 > 0:
                            collisions.append(Node("left", None, [x, y], None))
                        elif collision & 0x8 > 0:
                            collisions.append(Node("right", None, [x, y], None))
                    if collision & 0x10 > 0:
                        collisions.append(Node("ladder", None, [x, y], None))
                if hasPalettes:
                    color = self.tile_colors[index]
                    if color > 0:
                        tile_colors.append(Node("palette" + str(color), None, [x, y], None))
        if len(collisions) > 0:
            docs["collisions"] = collisions
        if hasPalettes and len(tile_colors) > 0:
            docs["tile-colors"] = tile_colors
        if len(self.script) > 0:
            script = Document(preserve_property_order=True)
            script.extend([Event.format(i, scene_names) for i in self.script])
            docs["init"] = script
        if len(self.player_hit1_script) > 0:
            script = Document(preserve_property_order=True)
            script.extend([Event.format(i, scene_names) for i in self.player_hit1_script])
            docs["player-hit-1"] = script
        if len(self.player_hit2_script) > 0:
            script = Document(preserve_property_order=True)
            script.extend([Event.format(i, scene_names) for i in self.player_hit2_script])
            docs["player-hit-2"] = script
        if len(self.player_hit3_script) > 0:
            script = Document(preserve_property_order=True)
            script.extend([Event.format(i, scene_names) for i in self.player_hit3_script])
            docs["player-hit-3"] = script
        return docs, scene_names
