import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import uuid
from uuid import UUID

from kdl import Document, Node, parse

from .actor import Actor
from .enums import SceneType
from .event import Event
from .marshalling import JsonSafe, serialize, Serializable
from .palette import Palette, PaletteID
from .trigger import Trigger
from .util import NameUtil, ProgressTracker, ProtoEvent, map_nodes, prop_node, sanitize_name


class SceneNameUtil(NameUtil):
    def __init__(self, parent: NameUtil):
        self.parent = parent
        self.id_to_actor = {}
        self.actor_to_id = {}
        self.id_to_trigger = {}
        self.trigger_to_id = {}
        self.actor_name_counts = {}
        self.trigger_name_counts = {}

    def add_actor(self, id: str, name: str, progress: ProgressTracker):
        if name == "player" or name == "$self$" or name.isdecimal():
            progress.log_error("Actor name '" + name + "' in scene '" + progress.current_scene
                               + "' may overlap with built-in names! Renaming to '" + name + "-'!")
            name += "-"
        if name in self.actor_name_counts:
            progress.log_error("Actor name '" + name + "' Already exists in scene '"
                               + progress.current_scene + "'! Renaming to '" + name + " "
                               + str(self.actor_name_counts[name] + 1) + "'!")
            self.actor_name_counts[name] += 1
            name += " " + str(self.actor_name_counts[name])
        else:
            self.actor_name_counts[name] = 1
        self.id_to_actor[id] = name
        self.actor_to_id[name] = id

    def add_trigger(self, id: str, name: str, progress: ProgressTracker):
        if name in self.trigger_name_counts:
            progress.log_error("Trigger name '" + name + "' Already exists in scene '" + progress.current_scene
                               + "! Renaming to '" + name + " " + str(self.trigger_name_counts[name] + 1) + "'!")
            self.trigger_name_counts[name] += 1
            name += " " + str(self.trigger_name_counts[name])
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

    def script_for_custom_event(self, id: str) -> List[ProtoEvent]:
        return self.parent.script_for_custom_event(id)

    def raw_custom_event_name(self, name: str) -> str:
        return self.parent.raw_custom_event_name(name)

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
    proj_index: int

    def serialize(self) -> JsonSafe:
        ret = {
            "id": serialize(self.id),
            "name": self.name,
            "backgroundId": serialize(self.background_id),
            "type": serialize(self.type),
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "paletteIds": self.palette_ids,
            "actors": serialize(self.actors),
            "triggers": serialize(self.triggers),
            "script": serialize(self.script),
            "playerHit1Script": serialize(self.player_hit1_script),
            "playerHit2Script": serialize(self.player_hit2_script),
            "playerHit3Script": serialize(self.player_hit3_script),
            "collisions": self.collisions,
            "tileColors": self.tile_colors
        }
        if self.notes is not None:
            ret["notes"] = self.notes
        if self.label_color is not None:
            ret["labelColor"] = self.label_color
        return ret

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe], proj_index: int) -> "Scene":
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
            actors=[Actor.deserialize(i, obj["actors"].index(i)) for i in obj["actors"]],
            triggers=[Trigger.deserialize(i, obj["triggers"].index(i)) for i in obj["triggers"]],
            collisions=obj["collisions"],
            tile_colors=obj["tileColors"] if "tileColors" in obj else [],
            script=[Event.deserialize(i) for i in obj["script"]],
            player_hit1_script=[Event.deserialize(i) for i in obj["playerHit1Script"]],
            player_hit2_script=[Event.deserialize(i) for i in obj["playerHit2Script"]],
            player_hit3_script=[Event.deserialize(i) for i in obj["playerHit3Script"]],
            proj_index=proj_index
        )

    def format(self, names: NameUtil, progress: ProgressTracker) -> Tuple[Dict[str, Document], NameUtil]:
        scene_names = SceneNameUtil(names)
        for actor in self.actors:
            if actor.name == "":
                scene_names.add_actor(str(actor.id), "actor-" + str(self.actors.index(actor)), progress)
            else:
                scene_names.add_actor(
                    str(actor.id),
                    sanitize_name(actor.name, names.scene_for_id(str(self.id)) + " actor"),
                    progress
                )
        for trigger in self.triggers:
            if trigger.name == "":
                scene_names.add_trigger(str(trigger.id), "trigger-" + str(self.triggers.index(trigger)), progress)
            else:
                scene_names.add_actor(
                    str(trigger.id),
                    sanitize_name(trigger.name, names.scene_for_id(str(self.id)) + " trigger"),
                    progress
                )
        meta = Document()
        meta.nodes.extend([
            prop_node("id", serialize(self.id)),
            prop_node("name", self.name),
            prop_node("type", self.type.serialize()),
            prop_node("background", scene_names.background_for_id(serialize(self.background_id))),
            prop_node("x", self.x),
            prop_node("y", self.y),
            prop_node("width", self.width),
            prop_node("height", self.height),
            prop_node("__index", self.proj_index)
        ])
        if len(self.palette_ids) > 0:
            meta.nodes.append(Node(
                name="palettes",
                nodes=[Node(
                    name="palette" + str(self.palette_ids.index(i)),
                    args=[names.palette_for_id(serialize(i))],
                ) for i in self.palette_ids if i is not None]
            ))
        if self.notes is not None:
            meta.nodes.append(prop_node("notes", self.notes))
        if self.label_color is not None:
            meta.nodes.append(prop_node("labelColor", self.label_color))
        docs = {"meta": meta}
        collisions = Document()
        tile_colors = Document()
        hasCollisions = len(self.collisions) > 0
        hasTileColors = len(self.tile_colors) > 0
        for y in range(self.height):
            for x in range(self.width):
                index = (self.width * y) + x
                if hasCollisions:
                    if index > len(self.collisions) - 1:
                        progress.log_error("Tried to access index " + str(index) + " of collision list "
                                           + str(len(self.collisions)) + " long in scene `" + self.name
                                           + "` ! This shouldn't be possible!")
                        break
                    collision = self.collisions[index]
                    if collision & 0xF == 0xF:
                        collisions.nodes.append(Node(name="all", args=[x, y]))
                    elif collision > 0:
                        if collision & 0x1 > 0:
                            collisions.nodes.append(Node(name="up", args=[x, y]))
                        elif collision & 0x2 > 0:
                            collisions.nodes.append(Node(name="down", args=[x, y]))
                        elif collision & 0x4 > 0:
                            collisions.nodes.append(Node(name="left", args=[x, y]))
                        elif collision & 0x8 > 0:
                            collisions.nodes.append(Node(name="right", args=[x, y]))
                    if collision & 0x10 > 0:
                        collisions.nodes.append(Node(name="ladder", args=[x, y]))
                if hasTileColors:
                    color = self.tile_colors[index]
                    if color > 0:
                        tile_colors.nodes.append(Node(name="palette" + str(color), args=[x, y]))
        if hasCollisions:
            docs["collisions"] = collisions
        if hasTileColors:
            docs["tile-colors"] = tile_colors
        if len(self.script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, scene_names) for i in self.script])
            docs["init"] = script
        if len(self.player_hit1_script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, scene_names) for i in self.player_hit1_script])
            docs["player-hit-1"] = script
        if len(self.player_hit2_script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, scene_names) for i in self.player_hit2_script])
            docs["player-hit-2"] = script
        if len(self.player_hit3_script) > 0:
            script = Document()
            script.nodes.extend([Event.format(i, scene_names) for i in self.player_hit3_script])
            docs["player-hit-3"] = script
        return docs, scene_names

    @staticmethod
    def parse(docs: Dict[str, Document], names: NameUtil, scene_dir: str, progress: ProgressTracker) -> "Scene":
        scene_names = SceneNameUtil(names)
        # Even more chicken-egg NameUtil hell! Aaaaaaaaaaaaaaaaaaaaa
        if os.path.exists(scene_dir + "/actors"):
            actor_dirs = [i.name for i in os.scandir(scene_dir + "/actors") if i.is_dir()]
            for i in actor_dirs:
                progress.set_status("Parsing meta for scene " + scene_dir.split("/")[-1] + " actor '" + i + "'")
                with open(scene_dir + "/actors/" + i + "/meta.kdl", encoding="utf-8") as meta:
                    contents = map_nodes(parse(meta.read()).nodes)
                    scene_names.add_actor(contents["id"], i, progress)
        else:
            actor_dirs = []
        if os.path.exists(scene_dir + "/triggers"):
            trigger_dirs = [i.name for i in os.scandir(scene_dir + "/triggers") if i.is_dir()]
            for i in trigger_dirs:
                progress.set_status("Parsing meta for scene " + scene_dir.split("/")[-1] + " trigger '" + i + "'")
                with open(scene_dir + "/triggers/" + i + "/meta.kdl", encoding="utf-8") as meta:
                    contents = map_nodes(parse(meta.read()).nodes)
                    scene_names.add_trigger(contents["id"], i, progress)
        else:
            trigger_dirs = []
        contents = map_nodes(docs["meta"].nodes)
        id = UUID(contents["id"]) if "id" in contents else uuid.uuid4()
        name = contents["name"]
        type = SceneType.deserialize(contents["type"])
        background_id = UUID(scene_names.id_for_background(contents["background"]))
        x = contents["x"]
        y = contents["y"]
        width = int(contents["width"])
        height = int(contents["height"])
        proj_index = int(contents["__index"])
        if "palettes" in contents:
            palettes = contents["palettes"]
            palette_ids: List[Optional[str]] = [None for _ in range(6)]
            for k, v in palettes.items():
                palette_ids[int(k[-1])] = names.id_for_palette(v)
        else:
            palette_ids = []
        notes = contents["notes"] if "notes" in contents else None
        label_color = contents["labelColor"] if "labelColor" in contents else None
        if "collisions" in docs:
            collisions = [0 for _ in range(width * height)]
            doc = docs["collisions"]
            for node in doc.nodes:
                node_x = node.args[0]
                node_y = node.args[1]
                index = int((width * node_y) + node_x)
                if node.name == "all":
                    collisions[index] |= 0xF
                elif node.name == "up":
                    collisions[index] |= 0x1
                elif node.name == "down":
                    collisions[index] |= 0x2
                elif node.name == "left":
                    collisions[index] |= 0x4
                elif node.name == "right":
                    collisions[index] |= 0x8
                elif node.name == "ladder":
                    collisions[index] |= 10
        else:
            collisions = []
        if "tile-colors" in docs:
            tile_colors = [0 for _ in range(width * height)]
            doc = docs["tile-colors"]
            for node in doc.nodes:
                node_x = node.args[0]
                node_y = node.args[1]
                index = int((width * node_y) + node_x)
                tile_colors[index] = int(node.name[-1])
        else:
            tile_colors = []
        if "init" in docs:
            script = [Event.parse(i, scene_names, progress) for i in docs["init"].nodes]
        else:
            script = []
        if "player-hit-1" in docs:
            player_hit1_script = [Event.parse(i, scene_names, progress) for i in docs["player-hit-1"].nodes]
        else:
            player_hit1_script = []
        if "player-hit-2" in docs:
            player_hit2_script = [Event.parse(i, scene_names, progress) for i in docs["player-hit-2"].nodes]
        else:
            player_hit2_script = []
        if "player-hit-3" in docs:
            player_hit3_script = [Event.parse(i, scene_names, progress) for i in docs["player-hit-3"].nodes]
        else:
            player_hit3_script = []
        # Finally time for the actors and triggers!
        actors: List[Optional[Actor]] = [None for _ in range(len(actor_dirs))]
        for dir in actor_dirs:
            progress.set_status("Parsing scripts for scene " + scene_dir.split("/")[-1] + " actor '" + dir + "'")
            actor_dir = scene_dir + "/actors/" + dir
            docs = {i.name[:-4]: parse(open(actor_dir + "/" + i.name, encoding="utf-8").read()) for i in os.scandir(actor_dir)
                    if i.is_file() and i.name.endswith(".kdl")}
            actor = Actor.parse(docs, scene_names, progress)
            actors[actor.scene_index] = actor
        triggers: List[Optional[Trigger]] = [None for _ in range(len(trigger_dirs))]
        for dir in trigger_dirs:
            progress.set_status("Parsing scripts for scene " + scene_dir.split("/")[-1] + " trigger '" + dir + "'")
            trigger_dir = scene_dir + "/triggers/" + dir
            docs = {i.name[:-4]: parse(open(trigger_dir + "/" + i.name, encoding="utf-8").read()) for i in os.scandir(trigger_dir)
                    if i.is_file() and i.name.endswith(".kdl")}
            trigger = Trigger.parse(docs, scene_names, progress)
            triggers[trigger.scene_index] = trigger
        return Scene(
            id=id,
            name=name,
            type=type,
            background_id=background_id,
            x=x,
            y=y,
            width=width,
            height=height,
            notes=notes,
            label_color=label_color,
            palette_ids=palette_ids,
            actors=actors,
            triggers=triggers,
            collisions=collisions,
            tile_colors=tile_colors,
            script=script,
            player_hit1_script=player_hit1_script,
            player_hit2_script=player_hit2_script,
            player_hit3_script=player_hit3_script,
            proj_index=proj_index
        )
