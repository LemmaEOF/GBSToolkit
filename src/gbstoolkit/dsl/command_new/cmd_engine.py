from collections import OrderedDict
from typing import Dict, Optional, Union

from .cmd_base import Command
from ..datatypes import UnionArgument
from ..enums import OverlayColor
from ..marshalling import JsonSafe
from ..util import NameUtil, NodeData

FIELD_NAMES = {
    "fade_style": "global/fadeStyle",
    "topdown_grid": "topDown/gridSize",
    "plat_min_vel": "platformer/minVelocity",
    "plat_walk_vel": "platformer/walkVelocity",
    "plat_run_vel": "platformer/runVelocity",
    "plat_walk_acc": "platformer/walkAcceleration",
    "plat_run_acc": "platformer/runAcceleration",
    "plat_dec": "platformer/deceleration",
    "plat_jump_vel": "platformer/jumpVelocity",
    "plat_grav": "platformer/gravity",
    "plat_hold_grav": "platformer/jumpGravity",
    "plat_max_fall_vel": "platformer/terminalVelocity"
}

INVERSE_FIELD_NAMES = {v: k for k, v in FIELD_NAMES.items()}


class EngineFieldSetCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ENGINE_FIELD_SET"

    @staticmethod
    def keyword() -> str:
        return "setEngineField"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"engineFieldKey": str, "value": Union[UnionArgument[int], UnionArgument[OverlayColor]]}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        value = UnionArgument.format(args["value"], names)
        if args["engineFieldKey"] == "fade_style" and type(value) == int:
            value = OverlayColor.format(value)
        return NodeData(OrderedDict(), [FIELD_NAMES[args["engineFieldKey"]], value])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        if data.args[0] == "global/fadeStyle":
            value = UnionArgument.parse(data.args[1], names, ("number", OverlayColor))
        else:
            value = UnionArgument.parse(data.args[1], names)
        return {"engineFieldKey": INVERSE_FIELD_NAMES[data.args[0]], "value": value}


class EngineFieldStoreCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ENGINE_FIELD_STORE"

    @staticmethod
    def keyword() -> str:
        return "storeEngineField"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"engineFieldKey": str, "value": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [FIELD_NAMES[args["engineFieldKey"]], "$" + args["value"] + "$"])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"engineFieldKey": INVERSE_FIELD_NAMES[data.args[0]], "value": data.args[1][1:-1]}
