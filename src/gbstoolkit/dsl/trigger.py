from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID

from .event import Event
from .marshalling import JsonSafe, serialize, Serializable


@dataclass
class Trigger(Serializable):
    id: UUID
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
            x=obj["x"],
            y=obj["y"],
            width=obj["width"],
            height=obj["height"],
            # trigger = obj["trigger"],
            notes=obj["notes"] if "notes" in obj else None,
            script=[Event.deserialize(i) for i in obj["script"]]
        )
