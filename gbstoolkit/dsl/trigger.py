from dataclasses import dataclass
from typing import Dict, List
from uuid import UUID

from event import Event
from marshalling import JsonSafe, serialize, Serializable


@dataclass
class Trigger(Serializable):
    id: UUID
    x: int
    y: int
    width: int
    height: int
    # trigger: str   TODO: is this actually a thing at all??? I can't find evidence that it's used anywhere
    script: List[Event]

    def serialize(self) -> JsonSafe:
        return {
            "id": serialize(self.id),
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            # "trigger": self.trigger,
            "script": serialize(self.script)
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Trigger":
        id = UUID(obj["id"])
        x = obj["x"]
        y = obj["y"]
        width = obj["width"]
        height = obj["height"]
        # trigger = obj["trigger"]
        script = [Event.deserialize(i) for i in obj["script"]]
        return Trigger(id=id, x=x, y=y, width=width, height=height, script=script)
