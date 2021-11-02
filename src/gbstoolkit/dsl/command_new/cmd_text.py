from collections import OrderedDict
from typing import Dict, List, Optional, Union
from uuid import UUID

from kdl import Node

from .cmd_base import Command
from ..marshalling import JsonSafe, serialize
from ..util import NameUtil, NodeData, format_dialogue, parse_dialogue


class MenuCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_MENU"

    @staticmethod
    def keyword() -> str:
        return "menu"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str, "items": int, "cancelOnB": bool, "layout": str, "cancelOnLastOption": bool}  # TODO: enum?

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(
            OrderedDict({
                "cancelOnB": args["cancelOnB"],
                "layout": args["layout"],
                "cancelOnLastOption": args["cancelOnLastOption"]
            }),
            ["$" + args["variable"] + "$"],
            [Node(name="option", args=[args["option" + str(i + 1)]]) for i in range(args["items"])]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"variable": data.args[0][1:-1], "items": len(data.children)}
        for node in data.children:
            ret["option"+str(data.children.index(node)+1)] = node.arguments[0]
        ret.update(
            cancelOnLastOption=data.props["cancelOLastOption"],
            cancelOnB=data.props["cancelOnB"],
            layout=data.props["layout"]
        )
        return ret

class TextDialogueCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_TEXT"

    @staticmethod
    def keyword() -> str:
        return "dialogue"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"text": Union[str, List[str]], "avatarId": Optional[UUID]}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        text = args["text"]
        node_args = [names.sprite_for_id(args["avatarId"])] if "avatarId" in args and args["avatarId"] != "" else []
        if type(text) == str:
            children = None
            node_args.append(format_dialogue(text))
        else:
            children = [Node(name="-", args=[format_dialogue(i)]) for i in text]
        ret = NodeData(OrderedDict(), node_args, children)
        return ret

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        if len(data.children) > 0:
            text = [parse_dialogue(i.args[0]) for i in data.children]
            avatar_id = data.args[0] if len(data.args) > 0 else None
        else:
            text = parse_dialogue(data.args[-1])
            avatar_id = data.args[0] if len(data.args) > 1 else None
        if avatar_id is not None:
            return {"avatarId": names.id_for_sprite(avatar_id), "text": text}
        else:
            return {"text": text}