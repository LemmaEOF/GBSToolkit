from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass
import platform
from queue import SimpleQueue
import re
from typing import Any, Dict, List, Optional, Union

from kdl import Document, Node

from .marshalling import JsonSafe, Serializable, serialize


# Weird median class to avoid circular refs, wheeee
@dataclass
class ProtoEvent:
    command: str
    args: Optional[Dict[str, JsonSafe]]
    children: Optional[Dict[str, List["ProtoEvent"]]]


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
    def script_for_custom_event(self, id: str) -> List[ProtoEvent]:
        return NotImplemented

    @abstractmethod
    def raw_custom_event_name(self, name: str) -> str:
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
    props: OrderedDict[str, Any]
    args: List[JsonSafe]
    children: Optional[List[Node]] = None


class ProgressTracker(ABC):
    def __init__(self):
        self._current_scene = None

    @property
    def current_scene(self):
        return self._current_scene

    @current_scene.setter
    def current_scene(self, val):
        self._current_scene = val

    @abstractmethod
    def set_status(self, status: str):
        return NotImplemented

    @abstractmethod
    def log_error(self, error: str):
        return NotImplemented

    @abstractmethod
    def flag_missing_command(self, command: str):
        return NotImplemented


class PrintProgressTracker(ProgressTracker):
    def __init__(self):
        super().__init__()
        self.known_missing_commands = []

    def set_status(self, status: str):
        print(status)

    def log_error(self, error: str):
        print("Error: " + error)

    def flag_missing_command(self, command: str):
        if command not in self.known_missing_commands:
            self.known_missing_commands.append(command)
            self.log_error("Attempted to parse unknown command '" + command
                           + "'. Arguments may be parsed incorrectly! If you are using a plugin, please let either "
                           + "LemmaEOF or the plugin dev know to add compat!")


class QueueProgressTracker(ProgressTracker):
    def __init__(self, status: SimpleQueue, errors: SimpleQueue):
        super().__init__()
        self.status = status
        self.errors = errors
        self.known_missing_commands = []

    def set_status(self, status: str):
        self.status.put(status)

    def log_error(self, error: str):
        self.errors.put(error)

    def flag_missing_command(self, command: str):
        if command not in self.known_missing_commands:
            self.known_missing_commands.append(command)
            self.errors.put("Attempted to parse unknown command '" + command
                            + "'. Arguments may be parsed incorrectly! If you are using a plugin, please let either "
                            + "LemmaEOF or the plugin dev know to add compat!")


class FormatError(Exception):
    """Exception raised when parsing .gbsproj JSON into KDL."""

    def __init__(self, context: str, element: Union[Serializable, JsonSafe], message: str):
        super().__init__()
        self.context = context
        self.element = element
        self.message = message


class ParseError(Exception):
    """Exception raised when parsing KDL into .gbsproj JSON."""

    def __init__(self, context: str, node: Node, message: str):
        super().__init__()
        self.context = context
        self.node = node
        self.message = message


def sanitize_name(name: str, context: str) -> str:
    illegal_filenames = ["CON", "PRN", "AUX", "CLOCK$", "NUL", "COM0", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6",
                         "COM7", "COM8", "COM9", "LPT0", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8",
                         "LPT9"]
    ret = re.sub(r'[/\\*:?\";|,\[\]&<>=\+]', '-', name)
    if platform.system() == "Windows" and ret.upper() in illegal_filenames:
        print("WARNING! " + context + " name '" + ret + "' is reserved on Windows. Renaming to '" + ret + "-" + "'!")
        print("For more information, see this video: https://youtu.be/bC6tngl0PTI")
        ret += "-"
    return ret


# TODO: more of these for safe parsing
def format_dialogue(text: str) -> str:
    return text.replace('Â…', '…')


def parse_dialogue(text: str) -> str:
    return text.replace('…', 'Â…').replace('\t', '')


def prop_node(name: str, value: Any) -> Node:
    return Node(name, args=[serialize(value)])


def map_nodes(doc: List[Node], ignore: List[str] = ()) -> Dict[str, JsonSafe]:
    return {i.name: i.args[0] if len(i.args) > 0 else map_nodes(i.nodes) for i in doc
            if (len(i.args) > 0 or len(i.nodes) > 0) and i.name not in ignore}


def command_to_keyword(name: str) -> str:
    parts = name.split('_')
    if len(parts) > 2:
        return parts[1].lower() + "".join([i.title() for i in parts[2:]])
    else:
        return parts[1].lower()


def keyword_to_command(name: str) -> str:
    return "EVENT_" + re.sub(r'(?<!^)(?=[A-Z])', '_', name).upper()
