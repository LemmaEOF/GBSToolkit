from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from uuid import UUID

from .marshalling import JsonSafe, serialize, Serializable

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

    @staticmethod
    def parse_id(id: Optional[str]) -> Optional[PaletteID]:
        if id is None:
            return None
        uuidtest = id.strip('{}').replace('-', '')
        if len(uuidtest) == 32:
            return UUID(id)
        else:
            return id

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Palette":
        id = Palette.parse_id(obj["id"])
        name = obj["name"]
        colors = obj["colors"]
        if "defaultName" in obj:
            return DefaultPalette(
                id=id,
                name=name,
                colors=colors,
                default_name=obj["defaultName"],
                default_colors=obj["defaultColors"]
            )
        else:
            return Palette(
                id=id,
                name=name,
                colors=colors
            )


@dataclass
class DefaultPalette(Palette):
    default_name: str
    default_colors: List[str]

    def serialize(self) -> JsonSafe:
        ret = super().serialize()
        ret["defaultName"] = self.default_name
        ret["defaultColors"] = self.default_colors
        return ret
