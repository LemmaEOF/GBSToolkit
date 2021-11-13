from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID
import uuid

from kdl import Node, Document

from .command import Command, Fallback, SwitchCommand, COMMANDS, KEYWORDS
from .marshalling import JsonSafe, serialize, Serializable
from .util import NameUtil, NodeData, ProtoEvent, ProgressTracker, FormatError, map_nodes, prop_node, keyword_to_command


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
        if self.args is not None and len(self.args) > 0:
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
        node_children = data.children if data.children is not None else []
        if self.children is not None and self.command.name() != "EVENT_CALL_CUSTOM_EVENT":
            if self.command is SwitchCommand:
                children_data = SwitchCommand.format_children_names(self.args)
                for k, v in children_data.items():
                    children_list = [i.format(names) for i in self.children[k]]
                    node = Node(name=v[0], props=v[1].props, args=v[1].args, nodes=children_list)
                    node_children.append(node)
            elif data.children is not None and len(data.children) > 0:
                if isinstance(self.command, Fallback):
                    fallback_children = []
                    for k, v in self.children.items():
                        children_list = [i.format(names) for i in v]
                        fallback_children.append(Node(name=k, nodes=children_list))
                    node_children.append(Node("__children", nodes=fallback_children))
                else:
                    raise FormatError("event", self, "")
            else:
                # TODO: special-case for Group, Loop, and setTimerScript (only one child, ever)
                for k, v in self.children.items():
                    children_list = [i.format(names) for i in v]
                    node_children.append(Node(name=k, nodes=children_list))
        props = data.props
        if props is None:
            print("Command " + self.command.name() + " is returning None props! This is ILLEGAL!")
        if self.args is not None:
            if "__collapse" in self.args:
                props["__collapse"] = self.args["__collapse"]
            if "__comment" in self.args:
                props["__comment"] = self.args["__comment"]
            if "__label" in self.args:
                props["__label"] = self.args["__label"]
        props["__eventid"] = str(self.id)
        if isinstance(self.command, Fallback):
            keyword = self.command.fallback_keyword
        else:
            keyword = self.command.keyword()
        return Node(name=keyword, props=props, args=data.args, nodes=node_children)

    @staticmethod
    def parse(node: Node, names: NameUtil, progress: ProgressTracker) -> "Event":
        command = KEYWORDS[node.name] if node.name in KEYWORDS else Fallback(keyword_to_command(node.name))
        children = None
        if command is SwitchCommand:
            child_nodes = SwitchCommand.parse_children_names(NodeData(node.props, node.args, node.nodes))
            children = {k: [Event.parse(i, names, progress) for i in v] for k, v in child_nodes}
        elif len(node.nodes) > 0 and command.children_names() is not None:
            # TODO: special-case for Group, Loop, and setTimerScript (only one child, ever)
            children = {}
            for child in node.nodes:
                children[child.name] = [Event.parse(i, names, progress) for i in child.nodes]
        elif isinstance(command, Fallback):
            children_nodes = [i for i in node.nodes if i.name == "__children"]
            if len(children_nodes) > 0:
                children = {}
                children_node = children_nodes[-1]
                for child in children_node.nodes:
                    children[child.name] = [Event.parse(i, names, progress) for i in child.nodes]
                node.nodes.remove(children_node)
        id = UUID(node.props["__eventid"]) if "__eventid" in node.props else uuid.uuid4()
        if isinstance(command, Fallback):
            progress.flag_missing_command(command.fallback_keyword)
        args = command.parse(NodeData(node.props, node.args, node.nodes), names)
        if args is None:
            args = {}
        if "__collapse" in node.props:
            args["__collapse"] = node.props["__collapse"]
        if "__comment" in node.props:
            args["__comment"] = node.props["__comment"]
        if "__label" in node.props:
            args["__label"] = node.props["__label"]
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
                    for k, v in proto.children.items()} if proto.children is not None else None
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
        doc = Document()
        doc.nodes.extend([
            prop_node("id", str(self.id)),
            prop_node("name", self.name),
            prop_node("description", self.description),
            prop_node("__index", self.proj_index)
        ])
        if len(self.variables) > 0:
            doc.nodes.append(Node(
                name="variables",
                nodes=[Node("$" + str(k) + "$", args=[v]) for k, v in self.variables.items()]
            ))
        if len(self.actors) > 0:
            doc.nodes.append(Node(
                name="actors",
                nodes=[Node(name="$" + str(k) + "$", args=[v]) for k, v in self.actors.items()]
            ))
        doc.nodes.append(Node(name="script", nodes=[i.format(names) for i in self.script]))
        return doc

    @staticmethod
    def parse(doc: Document, names: NameUtil, progress: ProgressTracker) -> "CustomEvent":
        contents = map_nodes(doc.nodes, ["script"])
        id = UUID(contents["id"]) if "id" in contents else uuid.uuid4()
        name = contents["name"]
        description = contents["description"]
        variables = {int(k[1:-1]): v for k, v in contents["variables"].items()} if "variables" in contents else {}
        actors = {int(k[1:-1]): v for k, v in contents["actors"].items()} if "actors" in contents else {}
        script_node = [i for i in doc.nodes if i.name == "script"][-1]
        script = [Event.parse(i, names, progress) for i in script_node.nodes]
        proj_index = int(contents["__index"])
        return CustomEvent(id, name, description, variables, actors, script, proj_index)
