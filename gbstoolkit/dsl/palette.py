from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from uuid import UUID

from kdl import Node

from .marshalling import JsonSafe, serialize, Serializable
from .util import NameUtil, map_nodes, prop_node

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

    def format(self, names: NameUtil) -> Node:
        nodes = [prop_node("id", serialize(self.id)), prop_node("name", self.name), Node(name="colors", nodes=[
            prop_node("white", self.colors[0]),
            prop_node("light", self.colors[1]),
            prop_node("dark", self.colors[2]),
            prop_node("black", self.colors[3])
        ])]
        return Node(name=names.palette_for_id(str(self.id)), nodes=nodes)

    @staticmethod
    def parse(node: Node) -> "Palette":
        children = map_nodes(node.nodes)
        name = children["name"]
        id = Palette.parse_id(children["id"])
        colors = [v for k, v in children["colors"].items()]
        if "defaultName" in children:
            default_name = children["defaultName"]
            default_colors = [v for k, v in children["defaultColors"].items()]
            return DefaultPalette(id=id, name=name, colors=colors, default_name=default_name,
                                  default_colors=default_colors)
        else:
            return Palette(id=id, name=name, colors=colors)

@dataclass
class DefaultPalette(Palette):
    default_name: str
    default_colors: List[str]

    def serialize(self) -> JsonSafe:
        ret = super().serialize()
        ret["defaultName"] = self.default_name
        ret["defaultColors"] = self.default_colors
        return ret

    def format(self, names: NameUtil) -> Node:
        nodes = [prop_node("id", serialize(self.id)), prop_node("name", self.name), Node(name="colors", nodes=[
            prop_node("white", self.colors[0]),
            prop_node("light", self.colors[1]),
            prop_node("dark", self.colors[2]),
            prop_node("black", self.colors[3])
        ]), prop_node("defaultName", self.default_name), Node(name="defaultColors", nodes=[
            prop_node("white", self.default_colors[0]),
            prop_node("light", self.default_colors[1]),
            prop_node("dark", self.default_colors[2]),
            prop_node("black", self.default_colors[3])
        ])]
        return Node(names.palette_for_id(self.id), nodes=nodes)
