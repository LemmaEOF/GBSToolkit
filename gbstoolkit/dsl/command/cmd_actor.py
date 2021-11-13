from collections import OrderedDict
from typing import Dict, Optional, Union
from uuid import UUID

from .cmd_base import Command
from ..datatypes import ActorID, UnionArgument
from ..enums import Direction, MoveType
from ..marshalling import JsonSafe, serialize
from ..util import NameUtil, NodeData

class ActorCollisionsDisableCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_COLLISIONS_DISABLE"

    @staticmethod
    def keyword() -> str:
        return "disableCollision"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0])}


class ActorCollisionsEnableCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_COLLISIONS_ENABLE"

    @staticmethod
    def keyword() -> str:
        return "enableCollision"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0])}


class ActorEmoteCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_EMOTE"

    @staticmethod
    def keyword() -> str:
        return "emote"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "emoteId": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"]), args["emoteId"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0]), "emoteId": data.args[1]}


class ActorGetDirectionCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_GET_DIRECTION"

    @staticmethod
    def keyword() -> str:
        return "storeDirection"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "direction": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"]), args["direction"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0]), "direction": data.args[1]}


class ActorGetPositionCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_GET_POSITION"

    @staticmethod
    def keyword() -> str:
        return "storePosition"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "vectorX": str, "VectorY": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"]), args["vectorX"], args["vectorY"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "actorId": names.id_for_actor(data.args[0]),
            "vectorX": data.args[1],
            "vectorY": data.args[2]
        }


class ActorHideCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_HIDE"

    @staticmethod
    def keyword() -> str:
        return "hide"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "actorId": names.id_for_actor(data.args[0])
        }


class ActorInvokeCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_INVOKE"

    @staticmethod
    def keyword() -> str:
        return "interactWith"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "actorId": names.id_for_actor(data.args[0])
        }


class ActorMoveRelativeCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_MOVE_RELATIVE"

    @staticmethod
    def keyword() -> str:
        return "moveBy"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        # x and y range -31 to 31
        return {"actorId": ActorID, "x": int, "y": int, "moveType": MoveType, "useCollisions": bool}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        if "verticalFirst" in args:
            args["moveType"] = "vertical" if args["verticalFirst"] else "horizontal"
        return NodeData(
            OrderedDict({"type": serialize(args["moveType"]), "collisions": args["useCollisions"]}),
            [names.actor_for_id(args["actorId"]), args["x"], args["y"]]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        if data.props is not None:
            type = MoveType.deserialize(data.props["type"])
            collisions = data.props["collisions"]
        else:
            type = MoveType.DIAGONAL
            collisions = False
        return {
            "actorId": names.id_for_actor(data.args[0]),
            "x": data.args[1],
            "y": data.args[2],
            "moveType": type.serialize(),
            "useCollisions": collisions
        }


class ActorMoveToCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_MOVE_TO"

    @staticmethod
    def keyword() -> str:
        return "moveTo"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        # x and y 0-255
        return {
            "actorId": ActorID,
            "x": UnionArgument[int],
            "y": UnionArgument[int],
            "moveType": MoveType,
            "useCollisions": bool
        }

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(
            OrderedDict({"type": serialize(args["moveType"]), "collisions": args["useCollisions"]}),
            [
                names.actor_for_id(args["actorId"]),
                UnionArgument.format(args["x"], names),
                UnionArgument.format(args["y"], names)
            ]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        if data.props is not None:
            type = MoveType.deserialize(data.props["type"])
            collisions = data.props["collisions"]
        else:
            type = MoveType.DIAGONAL
            collisions = False
        return {
            "actorId": names.id_for_actor(data.args[0]),
            "x": UnionArgument.parse(data.args[1], names),
            "y": UnionArgument.parse(data.args[2], names),
            "moveType": type.serialize(),
            "useCollisions": collisions
        }


class ActorPushCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_PUSH"

    @staticmethod
    def keyword() -> str:
        return "pushAway"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"continue": bool}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(args), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"continue": data.props["continue"]}


class ActorSetAnimateCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_ANIMATE"

    @staticmethod
    def keyword() -> str:
        return "setAnimate"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "animate": bool}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"]), args["animate"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0]), "animate": data.args[1]}


class ActorSetAnimationSpeedCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_ANIMATION_SPEED"

    @staticmethod
    def keyword() -> str:
        return "setAnimSpeed"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "animSpeed": Union[None, int]}  # range null and 0-4

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"]), args["animSpeed"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0]), "animSpeed": data.args[1]}


class ActorSetDirectionCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_DIRECTION"

    @staticmethod
    def keyword() -> str:
        return "setDirection"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "direction": UnionArgument[Direction]}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [
            names.actor_for_id(args["actorId"]),
            UnionArgument.format(args["direction"], names)
        ])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "actorId": names.id_for_actor(data.args[0]),
            "direction": UnionArgument.parse(data.args[1], names, ("direction", Direction))
        }


class ActorSetFrameCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_FRAME"

    @staticmethod
    def keyword() -> str:
        return "setFrame"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "frame": UnionArgument[int]}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [
            names.actor_for_id(args["actorId"]), UnionArgument.format(args["frame"], names)
        ])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0]), "frame": UnionArgument.parse(data.args[1], names)}


class ActorSetMovementSpeedCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_MOVEMENT_SPEED"

    @staticmethod
    def keyword() -> str:
        return "setMoveSpeed"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "speed": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"]), args["speed"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0]), "speed": data.args[1]}


class ActorSetPositionCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_POSITION"

    @staticmethod
    def keyword() -> str:
        return "setPosition"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "x": UnionArgument[int], "y": UnionArgument[int]}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(
            OrderedDict(),
            [
                names.actor_for_id(args["actorId"]),
                UnionArgument.format(args["x"], names),
                UnionArgument.format(args["y"], names)
            ]
        )

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "actorId": names.id_for_actor(data.args[0]),
            "x": UnionArgument.parse(data.args[1], names),
            "y": UnionArgument.parse(data.args[2], names)
        }


class ActorSetPositionRelativeCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_POSITION_RELATIVE"

    @staticmethod
    def keyword() -> str:
        return "changePosition"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "x": int, "y": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"]), args["x"], args["y"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0]), "x": data.args[1], "y": data.args[2]}


class ActorSetSpriteCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_SPRITE"

    @staticmethod
    def keyword() -> str:
        return "setSprite"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "spriteSheetId": UUID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"]), names.sprite_for_id(args["spriteSheetId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0]), "spriteSheetId": names.id_for_sprite(data.args[1])}


class ActorShowCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SHOW"

    @staticmethod
    def keyword() -> str:
        return "show"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0])}


class ActorStopUpdateScriptCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_STOP_UPDATE"

    @staticmethod
    def keyword() -> str:
        return "stopUpdate"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.actor_for_id(args["actorId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(data.args[0])}


class PlayerBounceCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_PLAYER_BOUNCE"

    @staticmethod
    def keyword() -> str:
        return "bounce"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"height": str}  # TODO: enum?

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["height"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
           "height": data.args[0]
        }


class PlayerSetSpriteCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_PLAYER_SET_SPRITE"

    @staticmethod
    def keyword() -> str:
        return "setPlayerSprite"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"spriteSheetId": UUID, "persist": bool}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"persist": args["persist"]}), [names.sprite_for_id(args["spriteSheetId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "spriteSheetId": names.id_for_sprite(data.args[0]),
            "persist": data.props["persist"]
        }


class SpritesHideCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SPRITES_HIDE"

    @staticmethod
    def keyword() -> str:
        return "hideAll"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class SpritesShowCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SPRITES_SHOW"

    @staticmethod
    def keyword() -> str:
        return "showAll"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None