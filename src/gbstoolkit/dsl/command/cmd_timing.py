from collections import OrderedDict
from typing import Dict, Optional, List

from .cmd_base import Command
from ..marshalling import JsonSafe
from ..util import NameUtil, NodeData


class TimerDisableCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_TIMER_DISABLE"

    @staticmethod
    def keyword() -> str:
        return "disableTimer"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class TimerRestartCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_TIMER_RESTART"

    @staticmethod
    def keyword() -> str:
        return "restartTimer"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class TimerSetScriptCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SET_TIMER_SCRIPT"

    @staticmethod
    def keyword() -> str:
        return "setTimerScript"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["script"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"duration": float}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"__scriptTabs": args["scriptTabs"]}), [args["duration"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"duration": data.args[0], "__scriptTabs": data.props["__scriptTabs"]}


class WaitCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_WAIT"

    @staticmethod
    def keyword() -> str:
        return "wait"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"time": float}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["time"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"time": data.args[0]}