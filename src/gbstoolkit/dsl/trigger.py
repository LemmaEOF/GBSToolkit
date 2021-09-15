from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID

from kdl import Document

from .event import Event
from .marshalling import JsonSafe, serialize, Serializable
from .util import NameUtil, prop_node, map_nodes


@dataclass
class Trigger(Serializable):
    id: UUID
    name: str
    x: int
    y: int
    width: int
    height: int
    # trigger: str   TODO: implement once it's actually a thing because oh lord I want it to be
    notes: Optional[str]
    script: List[Event]

    def serialize(self) -> JsonSafe:
        ret = {
            "id": serialize(self.id),
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            # "trigger": self.trigger,
            "script": serialize(self.script)
        }
        if self.notes is not None:
            ret["notes"] = self.notes
        return ret

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Trigger":
        return Trigger(
            id=UUID(obj["id"]),
            name=obj["name"] if "name" in obj else "",
            x=obj["x"],
            y=obj["y"],
            width=obj["width"],
            height=obj["height"],
            # trigger = obj["trigger"],
            notes=obj["notes"] if "notes" in obj else None,
            script=[Event.deserialize(i) for i in obj["script"]]
        )

    def format(self, names: NameUtil) -> Dict[str, Document]:
        meta = Document(preserve_property_order=True)
        meta.extend([
            prop_node("id", serialize(self.id)),
            prop_node("name", self.name),
            prop_node("x", self.x),
            prop_node("y", self.y),
            prop_node("width", self.width),
            prop_node("height", self.height),
            # prop_node("trigger", self.trigger),
        ])
        if self.notes is not None:
            meta.append(self.notes)
        docs = {"meta": meta}
        if len(self.script) > 0:
            script = Document(preserve_property_order=True)
            script.extend([Event.format(i, names) for i in self.script])
            docs["interact"] = script
        return docs

    @staticmethod
    def parse(docs: Dict[str, Document], names: NameUtil):
        meta = docs["meta"]
        contents = map_nodes(meta)
        script = [Event.parse(i, names) for i in docs["interact"]] if "interact" in docs else []
        return Trigger(
            id=UUID(contents["id"]),
            name=contents["name"] if "name" in contents else "",
            x=contents["x"],
            y=contents["y"],
            width=contents["width"],
            height=contents["height"],
            # trigger=contents["trigger"],
            notes=contents["notes"] if "notes" in contents else None,
            script=script
        )
