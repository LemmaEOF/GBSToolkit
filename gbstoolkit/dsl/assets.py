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