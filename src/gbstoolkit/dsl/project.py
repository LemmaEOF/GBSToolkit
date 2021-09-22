from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from kdl import Document, Node

from .assets import Background, SpriteSheet, Song
from .event import CustomEvent
from .marshalling import JsonSafe, serialize, Serializable
from .palette import Palette
from .scene import Scene
from .settings import Settings
from .util import NameUtil, prop_node, map_nodes, sanitize_name


class ProjectNameUtil(NameUtil):
    def __init__(self):
        self.id_to_background = {}
        self.background_to_id = {}
        self.id_to_custom_event = {}
        self.custom_event_to_id = {}
        self.id_to_palette = {}
        self.palette_to_id = {}
        self.id_to_scene = {}
        self.scene_to_id = {}
        self.id_to_song = {}
        self.song_to_id = {}
        self.id_to_sprite = {}
        self.sprite_to_id = {}
        self.custom_event_name_counts = {}
        self.palette_name_counts = {}
        self.scene_name_counts = {}

    def add_background(self, id: str, name: str):
        self.id_to_background[id] = name
        self.background_to_id[name] = id

    def add_custom_event(self, id: str, name: str):
        if name in self.custom_event_name_counts:
            print("Custom event name '" + name + "' Already exists! Renaming to `" + name + "-"
                  + str(self.custom_event_name_counts[name] + 1) + "`!")
            self.custom_event_name_counts[name] += 1
            name += "-" + str(self.custom_event_name_counts[name])
        else:
            self.custom_event_name_counts[name] = 1
        self.id_to_custom_event[id] = name
        self.custom_event_to_id[name] = id

    def add_palette(self, id: str, name: str):
        if name in self.palette_name_counts:
            print("Palette name '" + name + "' Already exists! Renaming to `" + name + "-"
                  + str(self.palette_name_counts[name] + 1) + "`!")
            self.palette_name_counts[name] += 1
            name += "-" + str(self.palette_name_counts[name])
        else:
            self.palette_name_counts[name] = 1
        self.id_to_palette[id] = name
        self.palette_to_id[name] = id

    def add_scene(self, id: str, name: str):
        if name in self.scene_name_counts:
            print("Scene name '" + name + "' Already exists! Renaming to " + name + "-"
                  + str(self.scene_name_counts[name] + 1))
            self.scene_name_counts[name] += 1
            name += "-" + str(self.scene_name_counts[name])
        else:
            self.scene_name_counts[name] = 1
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

    def custom_event_for_id(self, id: str) -> str:
        return self.id_to_custom_event[id]

    def id_for_custom_event(self, name: str) -> str:
        return self.custom_event_to_id[name]

    def palette_for_id(self, id: str) -> str:
        return self.id_to_palette[id]

    def id_for_palette(self, name: str) -> str:
        return self.palette_to_id[str]

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

    def trigger_for_id(self, id: str) -> str:
        return NotImplemented

    def id_for_trigger(self, name: str) -> str:
        return NotImplemented


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

    def format(self) -> Tuple[Dict[str, Document], NameUtil]:
        names = ProjectNameUtil()
        for background in self.backgrounds:
            names.add_background(str(background.id), background.name)
        for event in self.custom_events:
            if event.name == "":
                names.add_custom_event(str(event.id), "custom-event-" + str(self.custom_events.index(event)))
            else:
                names.add_custom_event(str(event.id), sanitize_name(event.name, "custom event"))
        for palette in self.palettes:
            if palette.name == "":
                names.add_palette(str(palette.id), "palette-" + str(self.palettes.index(palette)))
            else:
                names.add_palette(str(palette.id), sanitize_name(palette.name, "palette"))
        for scene in self.scenes:
            if scene.name == "":
                names.add_scene(str(scene.id), "scene-" + str(self.scenes.index(scene)))
            else:
                names.add_scene(str(scene.id), sanitize_name(scene.name, "scene"))
        for song in self.music:
            names.add_song(str(song.id), song.name)
        for sprite in self.sprite_sheets:
            names.add_sprite(str(sprite.id), sprite.name)
        meta = Document(preserve_property_order=True)
        meta.extend([
            prop_node("name", self.name),
            prop_node("author", self.author),
            prop_node("version", self.version),
            prop_node("release", self.release)
        ])
        if self.notes is not None:
            meta.append(prop_node("notes", self.notes))
        docs = {"project": meta}
        backgrounds = Document(preserve_property_order=True)
        backgrounds.extend([i.format() for i in self.backgrounds])
        docs["backgrounds"] = backgrounds
        sprite_sheets = Document(preserve_property_order=True)
        sprite_sheets.extend([i.format() for i in self.sprite_sheets])
        docs["sprite-sheets"] = sprite_sheets
        music = Document(preserve_property_order=True)
        music.extend([i.format() for i in self.music])
        docs["music"] = music
        variables = Document(preserve_property_order=True)
        variables.extend([Node("$" + k + "$", None, [v], None) for k, v in self.variables.items()])
        docs["variables"] = variables
        palettes = Document(preserve_property_order=True)
        palettes.extend([i.format(names) for i in self.palettes])
        docs["palettes"] = palettes
        # TODO: v3 fancy sprite sheets in separate folder!
        return docs, names
