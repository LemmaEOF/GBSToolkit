from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from uuid import UUID

from command import Command, COMMAND_TYPES
from marshalling import Variable, JsonSafe, serialize, Serializable


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
        args = evt["args"] if "args" in evt else None
        children = {k: [Event.deserialize(i) for i in v] for k, v in evt["children"]} if "children" in evt else None
        return Event(UUID(evt["id"]), COMMAND_TYPES[evt["command"]], args, children)

    def format(self):
        return self.command.format(self.args, self.children)

    @staticmethod
    def parse(text: str) -> "Event":
        return NotImplemented


@dataclass
class CustomEvent(Serializable):
    id: UUID
    name: str
    description: str
    variables: Dict[str, Variable]
    actors: Dict[str, Variable]
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
        id = UUID(obj["id"])
        name = obj["name"]
        description = obj["description"]
        variables = {k: Variable.deserialize(v) for k, v in obj["variables"]}
        actors = {k: Variable.deserialize(v) for k, v in obj["actors"]}
        script = [Event.deserialize(i) for i in obj["script"]]
        return CustomEvent(id=id, name=name, description=description, variables=variables, actors=actors, script=script)
