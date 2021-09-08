from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from uuid import UUID

from .datatypes import NamedKey
from .command import Command, COMMAND_TYPES
from .marshalling import JsonSafe, serialize, Serializable


@dataclass
class Event(Serializable):
    id: UUID
    command: Command
    args: Optional[Dict[str, Any]]
    children: Optional[Dict[str, List["Event"]]]

    def serialize(self) -> Dict[str, JsonSafe]:
        ret = {"id": str(self.id), "command": self.command.name()}
        if self.args is not None:
            ret["args"] = serialize(self.args)
        if self.children is not None:
            ret["children"] = serialize(self.children)
        return ret

    @staticmethod
    def deserialize(evt: Dict[str, JsonSafe]) -> "Event":
        return Event(
            id=UUID(evt["id"]),
            command=COMMAND_TYPES[evt["command"]] if evt["command"] in COMMAND_TYPES else None,  # FIXME later!
            args=evt["args"] if "args" in evt else None,
            children={k: [Event.deserialize(i) for i in v] for k, v in evt["children"].items()} if "children" in evt else None
        )

    def format(self) -> str:
        return self.command.format(self.args, self.children)

    @staticmethod
    def parse(text: str) -> "Event":
        return NotImplemented


@dataclass
class CustomEvent(Serializable):
    id: UUID
    name: str
    description: str
    variables: Dict[str, NamedKey]
    actors: Dict[str, NamedKey]
    script: List[Event]

    def serialize(self) -> JsonSafe:
        return {
            "id": serialize(self.id),
            "name": self.name,
            "description": self.description,
            "variables": serialize(self.variables),
            "actors": serialize(self.actors),
            "script": serialize(self.script)
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "CustomEvent":
        return CustomEvent(
            id=UUID(obj["id"]),
            name=obj["name"],
            description=obj["description"],
            variables={k: NamedKey.deserialize(v) for k, v in obj["variables"].items()},
            actors={k: NamedKey.deserialize(v) for k, v in obj["actors"].items()},
            script=[Event.deserialize(i) for i in obj["script"]]
        )
