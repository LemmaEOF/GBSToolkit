from collections import OrderedDict
from typing import Dict, Optional, Union
from uuid import UUID

from .cmd_base import Command
from ..enums import Direction
from ..marshalling import JsonSafe
from ..util import NameUtil, NodeData

class ScenePopAllStateCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SCENE_POP_ALL_STATE"

    @staticmethod
    def keyword() -> str:
        return "popAllScenes"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"fadeSpeed": str}  # why is it a string aaaaaaaa

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"fadeSpeed": int(args["fadeSpeed"])}), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "fadeSpeed": str(data.props["fadeSpeed"])
        }

class ScenePopStateCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SCENE_POP_STATE"

    @staticmethod
    def keyword() -> str:
        return "popScene"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"fadeSpeed": str}  # why is it a string aaaaaaaa

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"fadeSpeed": int(args["fadeSpeed"])}), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "fadeSpeed": str(data.props["fadeSpeed"])
        }


class ScenePushStateCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SCENE_PUSH_STATE"

    @staticmethod
    def keyword() -> str:
        return "pushScene"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class SceneResetStateCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SCENE_RESET_STATE"

    @staticmethod
    def keyword() -> str:
        return "clearSceneStack"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class SceneSwitchCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SWITCH_SCENE"

    @staticmethod
    def keyword() -> str:
        return "changeScene"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"sceneId": UUID, "x": int, "y": int, "direction": Direction, "fadeSpeed": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict()
        props["x"] = args["x"]
        props["y"] = args["y"]
        if args["direction"] != "":
            props["direction"] = args["direction"]
        props["fadeSpeed"] = args["fadeSpeed"]
        return NodeData(props, [names.scene_for_id(args["sceneId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "sceneId": names.id_for_scene(data.args[0]),
            "x": data.props["x"],
            "y": data.props["y"],
            "direction": data.props["direction"] if "direction" in data.props else "",
            "fadeSpeed": data.props["fadeSpeed"]
        }
