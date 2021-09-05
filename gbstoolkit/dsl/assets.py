from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
from uuid import UUID

from enums import SpriteSheetType
from marshalling import JsonSafe, serialize, Serializable


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
            "_v": self.timestamp.timestamp()
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Background":
        id = UUID(obj["id"])
        name = obj["name"]
        width = obj["width"]
        height = obj["height"]
        image_width = obj["imageWidth"]
        image_height = obj["imageHeight"]
        filename = obj["filename"]
        timestamp = datetime.fromtimestamp(obj["_v"])
        return Background(id=id, name=name, width=width, height=height, image_width=image_width,
                          image_height=image_height, filename=filename, timestamp=timestamp)


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
            "_v": self.timestamp.timestamp()
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "SpriteSheet":
        id = UUID(obj["id"])
        name = obj["name"]
        num_frames = obj["numFrames"]
        type = SpriteSheetType.deserialize(obj["type"])
        filename = obj["filename"]
        timestamp = datetime.fromtimestamp(obj["_v"])
        return SpriteSheet(id=id, name=name, num_frames=num_frames, type=type, filename=filename, timestamp=timestamp)


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
            "_v": self.timestamp.timestamp()
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Song":
        id = UUID(obj["id"])
        name = obj["name"]
        filename = obj["filename"]
        settings = obj["settings"]
        timestamp = datetime.fromtimestamp(obj["_v"])
        return Song(id=id, name=name, filename=filename, settings=settings, timestamp=timestamp)