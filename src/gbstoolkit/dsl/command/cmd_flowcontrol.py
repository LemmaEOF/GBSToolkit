from collections import OrderedDict
from typing import Dict, List, Optional, Tuple, Union
from uuid import UUID

from kdl import Node

from .cmd_base import Command
from ..datatypes import ActorID
from ..enums import Direction, RelativeActorPosition
from ..marshalling import JsonSafe, serialize
from ..util import NameUtil, NodeData


# TODO: single child so make it a direct child (in event.py)
class GroupCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_GROUP"

    @staticmethod
    def keyword() -> str:
        return "group"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class IfActorAtPositionCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_ACTOR_AT_POSITION"

    @staticmethod
    def keyword() -> str:
        return "ifActorAtPosition"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "x": int, "y": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            [names.actor_for_id(args["actorId"]), args["x"], args["y"]]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"actorId": names.id_for_actor(data.args[0]), "x": data.args[1], "y": data.args[2]}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfActorFacing(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_ACTOR_DIRECTION"

    @staticmethod
    def keyword() -> str:
        return "ifActorFacing"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "direction": Direction}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            [names.actor_for_id(args["actorId"]), args["direction"]]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"actorId": names.id_for_actor(data.args[0]), "direction": data.args[1]}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfActorRelativeTo(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_ACTOR_RELATIVE_TO_ACTOR"

    @staticmethod
    def keyword() -> str:
        return "ifActorRelativeTo"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "otherActorId": ActorID, "operation": RelativeActorPosition}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            [
                names.actor_for_id(args["actorId"]),
                RelativeActorPosition.format(args["operation"]),
                names.actor_for_id(args["otherActorId"])
            ]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {
            "actorId": names.id_for_actor(data.args[0]),
            "operation": RelativeActorPosition.parse(data.args[1]),
            "otherActorId": names.id_for_actor(data.args[2])
        }
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfColorSupportedCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_COLOR_SUPPORTED"

    @staticmethod
    def keyword() -> str:
        return "ifColorSupported"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            []
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfSavedDataCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_SAVED_DATA"

    @staticmethod
    def keyword() -> str:
        return "ifSaveExists"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            []
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfInputCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_INPUT"

    @staticmethod
    def keyword() -> str:
        return "ifAnyPressed"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"input": List[str]}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            args["input"]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"input": data.args}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfVariableCompareCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_VALUE_COMPARE"

    @staticmethod
    def keyword() -> str:
        return "ifCompareVars"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"vectorX": str, "operation": str, "vectorY": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            ["$" + args["vectorX"] + "$", args["operation"], "$" + args["vectorY"] + "$"]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"vectorX": data.args[0][1:-1], "operation": data.args[1], "vectorY": data.args[2][1:-1]}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfVariableFalseCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_FALSE"

    @staticmethod
    def keyword() -> str:
        return "ifFalse"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            ["$" + args["variable"] + "$"]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"variable": data.args[0][1:-1]}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfVariableFlagCompareCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_FLAGS_COMPARE"

    @staticmethod
    def keyword() -> str:
        return "ifFlag"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str, "flag": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            ["$" + args["variable"] + "$", args["flag"]]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"variable": data.args[0][1:-1], "flag": data.args[1]}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfVariableTrueCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_TRUE"

    @staticmethod
    def keyword() -> str:
        return "ifTrue"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            ["$" + args["variable"] + "$"]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"variable": data.args[0][1:-1]}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class IfValueCompareCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_IF_VALUE"

    @staticmethod
    def keyword() -> str:
        return "ifValue"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true", "false"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str, "operator": str, "comparator": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({})
        if "__disableElse" in args:
            props["__disableElse"] = args["__disableElse"]
        if "__collapseElse" in args:
            props["__collapseElse"] = args["__collapseElse"]
        return NodeData(
            props,
            ["$" + args["variable"] + "$", args["operator"], args["comparator"]]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"variable": data.args[0][1:-1], "operator": data.args[1], "comparator": data.args[2]}
        if "__disableElse" in data.props:
            ret["__disableElse"] = data.props["__disableElse"]
        if "__collapseElse" in data.props:
            ret["__collapseElse"] = data.props["__collapseElse"]
        return ret


class InputAwaitCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_AWAIT_INPUT"

    @staticmethod
    def keyword() -> str:
        return "awaitInput"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"input": List[str]}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), args["input"])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"input": data.args}


class InputScriptRemoveCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_REMOVE_INPUT_SCRIPT"

    @staticmethod
    def keyword() -> str:
        return "removeInputScript"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"input": List[str]}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), args["input"])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"input": data.args}


class InputScriptSetCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SET_INPUT_SCRIPT"

    @staticmethod
    def keyword() -> str:
        return "setInputScript"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"input": List[str], "persist": bool}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"persist": args["persist"] if "persist" in args else False}), args["input"])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"input": data.args, "persist": data.props["persist"] if "persist" in data.props else False}


class LabelDefineCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_DEFINE_LABEL"

    @staticmethod
    def keyword() -> str:
        return "label"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"label": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["label"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"label": data.args[0]}


class LabelGotoCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_GOTO_LABEL"

    @staticmethod
    def keyword() -> str:
        return "goto"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"label": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["label"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"label": data.args[0]}


# TODO: single child so make it a direct child (in event.py)
class LoopCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_LOOP"

    @staticmethod
    def keyword() -> str:
        return "loop"

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return ["true"]

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


# oh god oh fuck this is a mess
class SwitchCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SWITCH"

    @staticmethod
    def keyword() -> str:
        return "switch"

    @staticmethod  # TODO: fill out later this is gonna be *hell*
    def required_args() -> Optional[Dict[str, type]]:
        return None

    # TODO: THIS MAY END UP DELETING HIDDEN CONTENTS FROM THE JSON! RESEARCH ME ASAP!
    @staticmethod
    def format_children_names(args: Optional[Dict[str, JsonSafe]]) -> OrderedDict[str, Tuple[str, NodeData]]:
        ret = OrderedDict()
        for i in range(args["choices"]):
            value = args["value" + str(i)]
            collapse = args["__collapseCase" + str(i)]
            props = OrderedDict({"__collapse": True}) if collapse else OrderedDict()
            ret["true" + str(i)] = ("case", NodeData(props, [value]))
        if "__disableElse" not in args or not args["__disableElse"]:
            collapse = args["__collapseElse"]
            props = OrderedDict({"__collapse": True}) if collapse else OrderedDict()
            ret["false"] = ("default", NodeData(props, []))
        return ret

    @staticmethod
    def parse_children_names(data: NodeData) -> Dict[str, List[Node]]:
        ret = {}
        for i in data.children:
            if i.name == "case":
                ret["true" + str(data.children.index(i))] = i.nodes
            elif i.name == "default":
                ret["false"] = i.nodes
        return ret

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), ["$" + args["variable"] + "$"])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"variable": data.args[0][1:-1]}
        choices = 0
        has_default = False
        for i in data.children:
            if i.name == "case":
                choices += 1
                index = data.children.index(i)
                ret["value" + str(index)] = i.args[0]
                ret["__collapseCase" + str(index)] = i.props["__collapse"] if "__collapse" in i.props else False
            elif i.name == "default":
                has_default = True
                ret["__collapseElse"] = i.props["__collapse"] if "__collapse" in i.props else False
        ret["choices"] = choices
        ret["__disableElse"] = not has_default
        return ret
