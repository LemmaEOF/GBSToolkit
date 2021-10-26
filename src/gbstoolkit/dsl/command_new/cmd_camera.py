from collections import OrderedDict
from typing import Dict, Optional

from .cmd_base import Command
from ..enums import MoveType
from ..marshalling import JsonSafe
from ..util import NameUtil, NodeData

class CameraLockCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_CAMERA_LOCK"

    @staticmethod
    def keyword() -> str:
        return "lockCamera"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"speed": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["speed"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"speed": data.args[0]}


class CameraMoveToCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_CAMERA_MOVE_TO"

    @staticmethod
    def keyword() -> str:
        return "moveCameraTo"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"x": int, "y": int, "speed": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"speed": args["speed"]}), [args["x"], args["y"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"x": data.args[0], "y": data.args[1], "speed": data.props["speed"]}


class CameraShakeCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_CAMERA_SHAKE"

    @staticmethod
    def keyword() -> str:
        return "shakeCamera"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"shakeDirection": MoveType, "time": float}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["time"], args["shakeDirection"] if "shakeDirection" in args else "horizontal"])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"time": data.args[0], "shakeDirection": data.args[1]}