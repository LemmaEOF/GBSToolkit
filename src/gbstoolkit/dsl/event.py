from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID
import uuid

from kdl import Node, Document

from .command import Command, Fallback, COMMAND_TYPES, KEYWORDS
from .marshalling import JsonSafe, serialize, Serializable
from .util import NameUtil, NodeData, ParseError, FormatError, prop_node, upper_snake_caseify


# TODO: HOW THE HELL DO I COPE WITH THE NIGHTMARE THAT IS CUSTOM EVENTS AAAAAAAAAAAAAA
@dataclass
class Event(Serializable):
    id: UUID
    command: Command
    args: Optional[Dict[str, JsonSafe]]
    children: Optional[Dict[str, List["Event"]]]

    def serialize(self) -> Dict[str, JsonSafe]:
        if isinstance(self.command, Fallback):
            name = self.command.fallback_name
        else:
            name = self.command.name()
        ret = {"id": str(self.id), "command": name}
        if self.args is not None:
            ret["args"] = serialize(self.args)
        if self.children is not None:
            ret["children"] = serialize(self.children)
        return ret

    @staticmethod
    def deserialize(evt: Dict[str, JsonSafe]) -> "Event":
        return Event(
            id=UUID(evt["id"]),
            command=COMMAND_TYPES[evt["command"]] if evt["command"] in COMMAND_TYPES else Fallback(evt["command"]),
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
        if isinstance(self.command, Fallback):
            keyword = self.command.fallback_keyword
        else:
            keyword = self.command.keyword()
        return Node(name=keyword, properties=props, arguments=data.args, children=node_children)

    @staticmethod
    def parse(node: Node, names: NameUtil) -> "Event":
        command = KEYWORDS[node.name] if node.name in KEYWORDS else Fallback(upper_snake_caseify(node.name))
        children = None
        if node.children is not None and command.children_names() is not None:
            children = {}
            for child in node.children:
                children[child.name] = [Event.parse(i, names) for i in child.children]
        if node.properties is not None:
            id = UUID(node.properties["__eventid"]) if "__eventid" in node.properties else uuid.uuid4()
        else:
            id = uuid.uuid4()
        if isinstance(command, Fallback):
            print("WARNING! Attempting to parse unknown command " + command.fallback_name
                  + ". Arguments may be parsed incorrectly!")
            print("If you are using a plugin, please let either LemmaEOF or the plugin dev know to add compat!")
        args = command.parse(NodeData(node.properties, node.arguments, node.children), names)
        return Event(id=id, command=command, args=args, children=children)


@dataclass
class CustomEvent(Serializable):
    id: UUID
    name: str
    description: str
    variables: Dict[int, str]
    actors: Dict[int, str]
    script: List[Event]

    def serialize(self) -> JsonSafe:
        return {
            "id": serialize(self.id),
            "name": self.name,
            "description": self.description,
            "variables": {str(k): {"id": str(k), "name": v} for k, v in self.variables.items()},
            "actors": {str(k): {"id": str(k), "name": v} for k, v in self.actors.items()},
            "script": serialize(self.script)
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "CustomEvent":
        return CustomEvent(
            id=UUID(obj["id"]),
            name=obj["name"],
            description=obj["description"],
            variables={int(k): v["name"] for k, v in obj["variables"].items()},
            actors={int(k): v["name"] for k, v in obj["actors"].items()},
            script=[Event.deserialize(i) for i in obj["script"]]
        )

    def format(self, names: NameUtil) -> Document:
        doc = Document(preserve_property_order=True)
        doc.extend([
            prop_node("id", str(self.id)),
            prop_node("name", self.name),
            prop_node("description", self.description)
        ])
        doc.append(Node(
            "variables",
            None,
            None,
            [Node("$" + str(k) + "$", None, [v], None) for k, v in self.variables.items()]
        ))
        doc.append(Node(
            "actors",
            None,
            None,
            [Node("$" + str(k) + "$", None, [v], None) for k, v in self.variables.items()]
        ))
        doc.append(Node("script", None, None, [i.format(names) for i in self.script]))
        return doc
