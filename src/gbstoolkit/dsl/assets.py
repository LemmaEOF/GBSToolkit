from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
import uuid
from uuid import UUID

from kdl import Node

from .enums import SpriteSheetType
from .marshalling import JsonSafe, serialize, Serializable
from .util import prop_node, map_nodes


@dataclass
class Background(Serializable):
    id: UUID
    name: str
    width: int
    height: int
    image_width: int
    image_height: int
    filename: str
    timestamp: datetime

    def serialize(self) -> JsonSafe:
        return {
            "id": serialize(self.id),
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "imageWidth": self.image_width,
            "imageHeight": self.image_width,
            "filename": self.filename,
            "_v": int(self.timestamp.timestamp() * 1000)
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Background":
        return Background(
            id=UUID(obj["id"]),
            name=obj["name"],
            width=obj["width"],
            height=obj["height"],
            image_width=obj["imageWidth"],
            image_height=obj["imageHeight"],
            filename=obj["filename"],
            timestamp=datetime.fromtimestamp(obj["_v"] / 1000) if "_v" in obj else datetime.now()
        )

    def format(self) -> Node:
        nodes = [
            prop_node("id", serialize(self.id)),
            prop_node("width", self.width),
            prop_node("height", self.height),
            prop_node("imageWidth", self.image_width),
            prop_node("imageHeight", self.image_height),
            prop_node("filename", self.filename),
            prop_node("timesamp", self.timestamp.timestamp() * 1000)
        ]
        return Node(name=self.name, nodes=nodes)

    @staticmethod
    def parse(node: Node) -> "Background":
        contents = map_nodes(node.nodes)
        return Background(
            id=UUID(contents["id"]) if "id" in contents else uuid.uuid4(),
            name=node.name,
            width=contents["width"],
            height=contents["height"],
            image_width=contents["imageWidth"],
            image_height=contents["imageHeight"],
            filename=contents["filename"],
            timestamp=datetime.fromtimestamp(contents["timestamp"] / 1000) if "timestamp" in contents
            else datetime.now()
        )


@dataclass
class SpriteSheet(Serializable):  # TODO: gonna break entirely in v3! be ready!
    id: UUID
    name: str
    num_frames: int
    type: SpriteSheetType
    filename: str
    timestamp: datetime

    def serialize(self) -> JsonSafe:
        return {
            "id": serialize(self.id),
            "name": self.name,
            "numFrames": self.num_frames,
            "type": serialize(self.type),
            "filename": self.filename,
            "_v": int(self.timestamp.timestamp() * 1000)
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "SpriteSheet":
        return SpriteSheet(
            id=UUID(obj["id"]),
            name=obj["name"],
            num_frames=obj["numFrames"],
            type=SpriteSheetType.deserialize(obj["type"]),
            filename=obj["filename"],
            timestamp=datetime.fromtimestamp(obj["_v"] / 1000) if "_v" in obj else datetime.now()
        )

    def format(self) -> Node:
        nodes = [
            prop_node("id", serialize(self.id)),
            prop_node("numFrames", self.num_frames),
            prop_node("type", self.type.serialize()),
            prop_node("filename", self.filename),
            prop_node("timesamp", self.timestamp.timestamp() * 1000)
        ]
        return Node(name=self.name, nodes=nodes)

    @staticmethod
    def parse(node: Node) -> "SpriteSheet":
        contents = map_nodes(node.nodes)
        return SpriteSheet(
            id=UUID(contents["id"]) if "id" in contents else uuid.uuid4(),
            name=node.name,
            num_frames=contents["numFrames"],
            type=SpriteSheetType.deserialize(contents["type"]),
            filename=contents["filename"],
            timestamp=datetime.fromtimestamp(contents["timestamp"] / 1000) if "timestamp" in contents
            else datetime.now()
        )


@dataclass
class Song(Serializable):
    id: UUID
    name: str
    filename: str
    settings: Dict[str, Any]  # TODO: settings is unused in the sample project, idk what it does
    timestamp: datetime

    def serialize(self) -> JsonSafe:
        return {
            "id": serialize(self.id),
            "name": self.name,
            "settings": self.settings,
            "filename": self.filename,
            "_v": int(self.timestamp.timestamp() * 1000)
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Song":
        return Song(
            id=UUID(obj["id"]),
            name=obj["name"],
            filename=obj["filename"],
            settings=obj["settings"],
            timestamp=datetime.fromtimestamp(obj["_v"] / 1000) if "_v" in obj else datetime.now()
        )

    def format(self) -> Node:
        nodes = [
            prop_node("id", serialize(self.id)),
            prop_node("filename", self.filename),
            # prop_node("settings", ) TODO: can't do this bc I don't know what settings is
            prop_node("timesamp", self.timestamp.timestamp() * 1000)
        ]
        return Node(name=self.name, nodes=nodes)

    @staticmethod
    def parse(node: Node) -> "Song":
        contents = map_nodes(node.nodes)
        return Song(
            id=UUID(contents["id"]) if "id" in contents else uuid.uuid4(),
            name=node.name,
            filename=contents["filename"],
            settings={},  # TODO: can't do this bc I don't know what settings is
            timestamp=datetime.fromtimestamp(contents["timestamp"] / 1000) if "timestamp" in contents
            else datetime.now()
        )
