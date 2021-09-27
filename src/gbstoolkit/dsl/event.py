from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID
import uuid

from kdl import Node, Document

from .command import Command, Fallback, COMMANDS, KEYWORDS
from .marshalling import JsonSafe, serialize, Serializable
from .util import NameUtil, NodeData, ProtoEvent, ParseError, FormatError, map_nodes, prop_node, keyword_to_command


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
        ret = {"id": serialize(self.id), "command": name}
        if self.args is not None:
            ret["args"] = serialize(self.args)
        if self.children is not None:
            ret["children"] = serialize(self.children)
        return ret

    @staticmethod
    def deserialize(evt: Dict[str, JsonSafe]) -> "Event":
        return Event(
            id=UUID(evt["id"]),
            command=COMMANDS[evt["command"]] if evt["command"] in COMMANDS else Fallback(evt["command"]),
            args=evt["args"] if "args" in evt else None,
            children={k: [Event.deserialize(i) for i in v] for k, v in evt["children"].items()} if "children" in evt
            else None
        )

    def format(self, names: NameUtil) -> Node:
        data = self.command.format(self.args, names)
        node_children = data.children
        if self.children is not None and self.command.name != "EVENT_CALL_CUSTOM_EVENT":
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
        command = KEYWORDS[node.name] if node.name in KEYWORDS else Fallback(keyword_to_command(node.name))
        children = None
        if node.children is not None and (command.children_names() is not None or isinstance(command, Fallback)):
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
        if command.name() == "EVENT_CALL_CUSTOM_EVENT":
            children = {"script": [Event.deprotofy(i)
                                   for i in names.script_for_custom_event(args["customEventId"])]}
        return Event(id=id, command=command, args=args, children=children)

    def protofy(self) -> ProtoEvent:
        children = {k: [i.protofy() for i in v]
                    for k, v in self.children.items()} if self.children is not None else None
        return ProtoEvent(command=self.command.name(), args=self.args, children=children)

    @staticmethod
    def deprotofy(proto: ProtoEvent) -> "Event":
        children = {k: [Event.deprotofy(i) for i in v]
                    for k, v in proto.children.items()} if proto.children.items() is not None else None
        return Event(id=uuid.uuid4(), command=COMMANDS[proto.command], args=proto.args, children=children)


@dataclass
class CustomEvent(Serializable):
    id: UUID
    name: str
    description: str
    variables: Dict[int, str]
    actors: Dict[int, str]
    script: List[Event]
    proj_index: int

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
    def deserialize(obj: Dict[str, JsonSafe], proj_index: int) -> "CustomEvent":
        return CustomEvent(
            id=UUID(obj["id"]),
            name=obj["name"],
            description=obj["description"],
            variables={int(k): v["name"] for k, v in obj["variables"].items()},
            actors={int(k): v["name"] for k, v in obj["actors"].items()},
            script=[Event.deserialize(i) for i in obj["script"]],
            proj_index=proj_index
        )

    def format(self, names: NameUtil) -> Document:
        doc = Document(preserve_property_order=True)
        doc.extend([
            prop_node("id", str(self.id)),
            prop_node("name", self.name),
            prop_node("description", self.description),
            prop_node("__index", self.proj_index)
        ])
        if len(self.variables) > 0:
            doc.append(Node(
                "variables",
                None,
                None,
                [Node("$" + str(k) + "$", None, [v], None) for k, v in self.variables.items()]
            ))
        if len(self.actors) > 0:
            doc.append(Node(
                "actors",
                None,
                None,
                [Node("$" + str(k) + "$", None, [v], None) for k, v in self.variables.items()]
            ))
        doc.append(Node("script", None, None, [i.format(names) for i in self.script]))
        return doc

    @staticmethod
    def parse(doc: Document, names: NameUtil) -> "CustomEvent":
        contents = map_nodes(doc)
        id = UUID(contents["id"]) if "id" in contents else uuid.uuid4()
        name = contents["name"]
        description = contents["description"]
        variables = {int(k[1:-1]): v for k, v in contents["variables"].items()} if "variables" in contents else {}
        actors = {int(k[1:-1]): v for k, v in contents["actors"].items()} if "actors" in contents else {}
        script_node = [i for i in doc if i.name == "script"][0]
        script = [Event.parse(i, names) for i in script_node]
        proj_index = contents["__index"]
        return CustomEvent(id, name, description, variables, actors, script, proj_index)
