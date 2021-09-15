from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID
import uuid

from kdl import Node

from .datatypes import NamedKey
from .command import Command, COMMAND_TYPES, KEYWORDS
from .marshalling import JsonSafe, serialize, Serializable
from .util import NameUtil, NodeData, ParseError, FormatError


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
            children={k: [Event.deserialize(i) for i in v] for k, v in evt["children"].items()} if "children" in evt
            else None
        )

    def format(self, names: NameUtil) -> Node:
        data = self.command.format(self.args, names)
        node_children = data.children
        if self.children is not None:
            if data.children is not None:
                raise FormatError("event", self, "")
            node_children = []
            for k, v in self.children.items():
                children_list = [i.format(names) for i in v]
                node_children.append(Node(name=k, properties=None, arguments=None, children=children_list))
        props = data.props if data.props is not None else {}
        props["__eventid"] = str(self.id)
        return Node(name=self.command.keyword(), properties=props, arguments=data.args, children=node_children)

    @staticmethod
    def parse(node: Node, names: NameUtil) -> "Event":
        command = KEYWORDS[node.name]
        children = None
        if node.children is not None and command.children_names() is not None:
            children = {}
            for child in node.children:
                children[child.name] = [Event.parse(i, names) for i in child.children]
        if node.properties is not None:
            id = UUID(node.properties["__eventid"]) if "__eventid" in node.properties else uuid.uuid4()
        else:
            id = uuid.uuid4()
        args = command.parse(NodeData(node.properties, node.arguments, node.children), names)
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
