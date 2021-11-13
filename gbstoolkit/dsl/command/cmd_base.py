from abc import ABC, ABCMeta, abstractmethod
from collections import OrderedDict
from typing import Dict, List, Optional

from kdl import Node

from ..marshalling import JsonSafe
from ..util import NameUtil, NodeData, command_to_keyword

COMMANDS: Dict[str, "Command"] = {}  # Fills in automatically by subclassing Command! woooo

KEYWORDS: Dict[str, "Command"] = {}


# Should only ever autoregister Command instances, so if not then we've got a looot more problems on our hands
class AutoRegister(ABCMeta):
    # welcome to metaprogramming hell!
    # noinspection PyTypeChecker
    def __init__(cls, name, bases, clsdict):
        if len(cls.mro()) == 4 and "name" in clsdict and "keyword" in clsdict:
            COMMANDS[cls.name()] = cls
            KEYWORDS[cls.keyword()] = cls
        super(AutoRegister, cls).__init__(name, bases, clsdict)

    @staticmethod
    def name() -> str:
        pass

    @staticmethod
    def keyword() -> str:
        pass


class Command(ABC, metaclass=AutoRegister):
    @staticmethod
    @abstractmethod
    def name() -> str:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def keyword() -> str:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return None

    @staticmethod
    @abstractmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return NotImplemented


class EndCommand(Command):  # TODO: good way to strip out of things/append automatically?
    @staticmethod
    def name() -> str:
        return "EVENT_END"

    @staticmethod
    def keyword() -> str:
        return "end"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


# TODO: make me use JiK?
class Fallback(Command):
    def __init__(self, name: str):
        self.fallback_name = name
        self.fallback_keyword = command_to_keyword(name)

    @staticmethod
    def name() -> str:
        return ""

    @staticmethod
    def keyword() -> str:
        return ""

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        if args is not None:
            children = []
            for k, v in args.items():
                if isinstance(v, dict):
                    data = Fallback.format(v, names)
                    children.append(Node(name=k, props=data.props, args=data.args, nodes=data.children))
                elif isinstance(v, list):
                    children.append(Node(
                        name=k,
                        props=OrderedDict({"__type": "list"}),
                        nodes=Fallback.format_list(v, names))
                    )
                else:
                    children.append(Node(name=k, args=[v]))
            return NodeData(OrderedDict(), [], children)
        return NodeData(OrderedDict(), [], None)

    @staticmethod
    def format_list(entries: List[JsonSafe], names: NameUtil) -> List[Node]:
        ret = []
        for i in entries:
            if isinstance(i, dict):
                ret.append(Node(name="-", nodes=Fallback.format(i, names).children))
            elif isinstance(i, list):
                ret.append(Node(name="-", props=OrderedDict({"__type": "list"}), nodes=Fallback.format_list(i, names)))
            else:
                ret.append(Node(name="-", args=[i]))
        return ret

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {}
        if data.children is not None:
            for node in data.children:
                if node.nodes is not None:
                    if node.props is not None and "__type" in node.props and node.props["__type"] == "list":
                        ret[node.name] = Fallback.parse_list(node.nodes, names)
                    else:
                        if node.name != "__collapse" and node.name != "__comment" and node.name != "__label":
                            ret[node.name] = Fallback.parse(NodeData(OrderedDict(), [], node.nodes), names)
                else:
                    ret[node.name] = node.args[0]
        return ret

    @staticmethod
    def parse_list(children: List[Node], names: NameUtil) -> List[JsonSafe]:
        ret = []
        for node in children:
            if node.nodes is not None:
                if node.props is not None and "__type" in node.props and node.props["__type"] == "list":
                    ret.append(Fallback.parse_list(node.nodes, names))
                else:
                    ret.append(Fallback.parse(NodeData(OrderedDict(), [], node.nodes), names))
            else:
                ret.append(node.args[0])
        return ret