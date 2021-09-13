from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from uuid import UUID
import uuid

from kdl import Node

from .datatypes import NamedKey
from .command import Command, COMMAND_TYPES, KEYWORDS
from .marshalling import JsonSafe, serialize, Serializable
from .util import NameUtil


@dataclass
class Event(Serializable):
    id: UUID
    command: Command
    args: Optional[Dict[str, JsonSafe]]
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

    def format(self, names: NameUtil) -> Node:
        outputs = self.command.format(self.args, names)
        node_children = None
        if self.children is not None:
            node_children = []
            for k, v in self.children.items():
                children_list = [i.format(names) for i in v]
                node_children.append(Node(name=k, properties=None, arguments=None, children=children_list))
        properties = outputs[0] if outputs[0] is not None else {}
        properties["__uuid__"] = str(self.id)
        return Node(name=self.command.keyword(), properties=properties, arguments=outputs[1], children=node_children)

    @staticmethod
    def parse(node: Node, names: NameUtil) -> "Event":
        children = None
        if node.children is not None:
            children = {}
            for child in node.children:
                children[child.name] = [Event.parse(i, names) for i in child.children]
        command = KEYWORDS[node.name]
        id = UUID(node.properties["__uuid__"]) if "__uuid__" in node.properties else uuid.uuid4()
        args = command.parse(node.properties, node.arguments, names)
        return Event(id=id, command=command, args=args, children=children)


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
