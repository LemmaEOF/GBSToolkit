from collections import OrderedDict
from typing import Dict, List, Optional, Union
from uuid import UUID

from kdl import Node

from .cmd_base import Command
from ..datatypes import ActorID, UnionArgument
from ..enums import OverlayColor
from ..marshalling import JsonSafe, serialize
from ..util import NameUtil, NodeData


class CallCustomEventCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_CALL_CUSTOM_EVENT"

    @staticmethod
    def keyword() -> str:
        return "call"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"customEventId": UUID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        if len(args) > 2:
            props = OrderedDict({})
            for k, v in args.items():
                if "variable" in k:
                    props["var" + k[10:-2]] = "$" + v + "$"
                elif "actor" in k:
                    props["actor" + k[7:-2]] = names.actor_for_id(v)
        else:
            props = None
        return NodeData(props, [names.custom_event_for_id(args["customEventId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {
            "customEventId": names.id_for_custom_event(data.args[0]),
            "__name": names.raw_custom_event_name(data.args[0])
        }
        if data.props is not None:
            for k, v in data.props.items():
                if k.startswith("var"):
                    ret["$variable[" + k[3:] + "]$"] = v[1:-1]
                elif k.startswith("actor"):
                    ret["$actor[" + k[5:] + "]$"] = names.id_for_actor(v)
        return ret


class CommentCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_COMMENT"

    @staticmethod
    def keyword() -> str:
        return "note"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"text": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["text"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"text": data.args[0]}


class DataClearCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_DATA_CLEAR"

    @staticmethod
    def keyword() -> str:
        return "clearSave"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class DataLoadCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_DATA_LOAD"

    @staticmethod
    def keyword() -> str:
        return "loadSave"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class DataSaveCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_DATA_SAVE"

    @staticmethod
    def keyword() -> str:
        return "createSave"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


# TODO: this is hell we live in hell why does this have six args one of which is a list (impl me later)
# commenting out so it uses fallback for now
# class LaunchProjectileCommand(Command):
#     @staticmethod
#     def name() -> str:
#         return "EVENT_LAUNCH_PROJECTILE"
#
#     @staticmethod
#     def keyword() -> str:
#         return "launchProjectile"
#
#     @staticmethod
#     def required_args() -> Optional[Dict[str, type]]:
#         return {
#             "spriteSheetId": UUID,
#             "actorId": ActorID,
#             "direction": UnionArgument[Direction],
#             "speed": int,
#             "collisionGroup": str,
#             "collisionMask": List[str]
#         }
#
#     @staticmethod
#     def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
#         pass
#
#     @staticmethod
#     def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
#         pass


class MusicPlayCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_MUSIC_PLAY"

    @staticmethod
    def keyword() -> str:
        return "playMusic"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"musicId": UUID, "loop": bool}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"loop": args["loop"]}), [names.song_for_id(args["musicId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"musicId": names.id_for_song(data.args[0]), "loop": data.props["loop"]}


class MusicStopCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_MUSIC_STOP"

    @staticmethod
    def keyword() -> str:
        return "stopMusic"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class OverlayHideCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_OVERLAY_HIDE"

    @staticmethod
    def keyword() -> str:
        return "hideOverlay"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class OverlayMoveToCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_OVERLAY_MOVE_TO"

    @staticmethod
    def keyword() -> str:
        return "moveOverlay"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"x": int, "y": int, "speed": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"speed": args["speed"]}), [args["x"], args["y"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"x": data.args[0], "y": data.args[1], "speed": data.props["speed"]}


class OverlayShowCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_OVERLAY_SHOW"

    @staticmethod
    def keyword() -> str:
        return "showOverlay"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"color": OverlayColor, "x": int, "y": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"color": args["color"]}), [args["x"], args["y"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "x": data.args[0],
            "y": data.args[1],
            "color": data.props["color"] if "color" in data.props else "black"
        }