from dataclasses import dataclass
from typing import List, Union
from uuid import UUID

from marshalling import JsonSafe, serialize, Serializable

PaletteID = Union[str, UUID]


@dataclass
class Palette(Serializable):
    id: PaletteID  # string for default palettes!
    name: str
    colors: List[str]

    def serialize(self) -> JsonSafe:
        return {
            "id": serialize(self.id),
            "name": self.name,
            "colors": self.colors
        }


@dataclass
class DefaultPalette(Palette):
    default_name: str
    default_colors: List[str]

    def serialize(self) -> JsonSafe:
        ret = super().serialize()
        ret["defaultName"] = self.default_name
        ret["defaultColors"] = self.default_colors
        return ret