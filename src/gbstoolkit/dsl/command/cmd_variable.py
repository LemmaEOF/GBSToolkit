from collections import OrderedDict
from typing import Dict, Optional

from .cmd_base import Command
from ..datatypes import UnionArgument
from ..marshalling import JsonSafe
from ..util import NameUtil, NodeData


class VariableAddFlagsCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ADD_FLAGS"

    @staticmethod
    def keyword() -> str:
        return "addFlags"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {
            "variable": str,
            "flag1": bool,
            "flag2": bool,
            "flag3": bool,
            "flag4": bool,
            "flag5": bool,
            "flag6": bool,
            "flag7": bool,
            "flag8": bool
        }

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        nargs = ["$" + args["variable"] + "$"]
        nargs.extend([i+1 for i in range(8) if args["flag" + str(i+1)]])
        return NodeData(OrderedDict(), nargs)

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"variable": data.args[0][1:-1]}
        ret.update({"flag" + str(i+1): True if i+1 in data.props else False for i in range(8)})
        return ret


class VariableClearFlagsCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_CLEAR_FLAGS"

    @staticmethod
    def keyword() -> str:
        return "clearFlags"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {
            "variable": str,
            "flag1": bool,
            "flag2": bool,
            "flag3": bool,
            "flag4": bool,
            "flag5": bool,
            "flag6": bool,
            "flag7": bool,
            "flag8": bool
        }

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        nargs = ["$" + args["variable"] + "$"]
        nargs.extend([i+1 for i in range(8) if args["flag" + str(i+1)]])
        return NodeData(OrderedDict(), nargs)

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"variable": data.args[0][1:-1]}
        ret.update({"flag" + str(i+1): True if i+1 in data.props else False for i in range(8)})
        return ret


class VariableDecCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_DEC_VALUE"

    @staticmethod
    def keyword() -> str:
        return "decrement"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["variable"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"variable": data.args[0][1:-1]}


class VariableIncCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_INC_VALUE"

    @staticmethod
    def keyword() -> str:
        return "increment"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["variable"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"variable": data.args[0][1:-1]}


class VariableMathCommand(Command):  # This one's a fun one!
    key_to_symbol = {"set": "=", "add": "+", "sub": "-", "mul": "*", "div": "/", "mod": "%"}
    symbol_to_key = {v: k for k, v in key_to_symbol.items()}

    @staticmethod
    def name() -> str:
        return "EVENT_VARIABLE_MATH"

    @staticmethod
    def keyword() -> str:
        return "calculate"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"vectorX": str, "operation": str, "other": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict()
        nargs = ["$" + args["vectorX"] + "$", VariableMathCommand.key_to_symbol[args["operation"]]]
        other_type = args["other"]
        if other_type == "true":
            nargs.append(True)
        elif other_type == "false":
            nargs.append("False")
        elif other_type == "var":
            nargs.append("$" + args["vectorY"] + "$")
        elif other_type == "val":
            nargs.append(args["value"])
        elif other_type == "rnd":
            nargs.append(str(args["minValue"]) + "-" + str(args["maxValue"]))  # TODO: is there a better way to do this?
        else:
            raise RuntimeError("Unknown other type for variable math! How is that possible?")  # TODO: better error?
        if "clamp" in args:
            props["clamp"] = args["clamp"]
        return NodeData(props, nargs)

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"vectorX": data.args[0][1:-1], "operation": VariableMathCommand.symbol_to_key[data.args[1]]}
        other = data.args[2]
        if other is True:
            ret["other"] = "true"
        elif other is False:
            ret["other"] = "false"
        elif type(other) == int:  # TODO: hopefully this will be an int? figure this out soon!
            ret["other"] = "val"
            ret["value"] = other
        elif type(other) == str:
            if other[0] == "$" and other[-1] == "$":
                ret["other"] = "var"
                ret["vectorY"] = other[1:-1]
            elif "-" in other:
                sides = other.split("-")
                ret["other"] = "rnd"
                ret["minValue"] = int(sides[0])
                ret["maxValue"] = int(sides[1])
            else:
                raise RuntimeError("Unknown other type for variable math!")
        else:
            raise RuntimeError("Unknown other type for variable math!")
        if "clamp" in data.props:
            ret["clamp"] = data.props["clamp"]
        return ret


class VariableSetFlagsCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SET_FLAGS"

    @staticmethod
    def keyword() -> str:
        return "setFlags"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {
            "variable": str,
            "flag1": bool,
            "flag2": bool,
            "flag3": bool,
            "flag4": bool,
            "flag5": bool,
            "flag6": bool,
            "flag7": bool,
            "flag8": bool
        }

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        nargs = ["$" + args["variable"] + "$"]
        nargs.extend([args["flag" + str(i+1)] for i in range(8)])
        return NodeData(OrderedDict(), nargs)

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"variable": data.args[0][1:-1]}
        ret.update({"flag" + str(i+1): data.args[i+1] for i in range(8)})
        return ret


class VariableSetFalseCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SET_FALSE"

    @staticmethod
    def keyword() -> str:
        return "setFalse"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), ["$" + args["variable"] + "$"])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"variable": data.args[0][1:-1]}


class VariableSetTrueCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SET_TRUE"

    @staticmethod
    def keyword() -> str:
        return "setTrue"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), ["$" + args["variable"] + "$"])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"variable": data.args[0][1:-1]}


class VariableSetValueCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SET_VALUE"

    @staticmethod
    def keyword() -> str:
        return "setValue"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"variable": str, "value": UnionArgument[int]}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), ["$" + args["variable"] + "$", UnionArgument.format(args["value"], names)])


    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"variable": data.args[0][1:-1], "value": UnionArgument.parse(data.args[1], names)}


class VariablesResetCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_RESET_VARIABLES"

    @staticmethod
    def keyword() -> str:
        return "resetVariables"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None
