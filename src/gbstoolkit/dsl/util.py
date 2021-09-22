from abc import ABC, abstractmethod
from dataclasses import dataclass
import platform
import re
from typing import Any, Dict, List, Optional, Union

from kdl import Document, Node

from .marshalling import JsonSafe, Serializable, serialize


class NameUtil(ABC):

    @abstractmethod
    def actor_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_actor(self, name: str) -> str:
        return NotImplemented

    @abstractmethod
    def background_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_background(self, name: str) -> str:
        return NotImplemented

    @abstractmethod
    def custom_event_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_custom_event(self, name: str) -> str:
        return NotImplemented

    @abstractmethod
    def palette_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_palette(self, name: str) -> str:
        return NotImplemented

    @abstractmethod
    def scene_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_scene(self, name: str) -> str:
        return NotImplemented

    @abstractmethod
    def song_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_song(self, name: str) -> str:
        return NotImplemented

    @abstractmethod
    def sprite_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_sprite(self, name: str) -> str:
        return NotImplemented

    @abstractmethod
    def trigger_for_id(self, id: str) -> str:
        return NotImplemented

    @abstractmethod
    def id_for_trigger(self, name: str) -> str:
        return NotImplemented


@dataclass
class NodeData:
    props: Optional[Dict[str, JsonSafe]]
    args: Optional[List[JsonSafe]]
    children: Optional[List[Node]] = None


class FormatError(Exception):
    """Exception raised when parsing .gbsproj JSON into KDL."""

    def __init__(self, context: str, element: Union[Serializable, JsonSafe], message: str):
        self.context = context
        self.element = element
        self.message = message


class ParseError(Exception):
    """Exception raised when parsing KDL into .gbsproj JSON."""

    def __init__(self, context: str, node: Node, message: str):
        self.context = context
        self.node = node
        self.message = message


def sanitize_name(name: str, context: str) -> str:
    illegal_filenames = ["CON", "PRN", "AUX", "CLOCK$", "NUL", "COM0", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6",
                         "COM7", "COM8", "COM9", "LPT0", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8",
                         "LPT9"]
    ret = re.sub(r'[/\\*:?\";|,\[\]&<>= ]', '-', name.lower())
    if platform.system() == "Windows" and ret in illegal_filenames:
        print("WARNING! " + context + " name '" + ret + "' is reserved on Windows. Renaming to '" + ret + "-" + "'!")
        print("For more information, see this video: https://youtu.be/bC6tngl0PTI")
        ret += "-"
    return ret


def prop_node(name: str, value: Any) -> Node:
    return Node(name, None, [serialize(value)], None)


def map_nodes(doc: Union[Document, List[Node]]) -> Dict[str, JsonSafe]:
    return {i.name: i.arguments[0] if len(i.arguments) > 0 else map_nodes(i.children) for i in doc}


def camel_caseify(name: str) -> str:
    parts = name.split('_')
    return parts[1].lower() + "".join([i.title() for i in parts[2:]])


def upper_snake_caseify(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).upper()
