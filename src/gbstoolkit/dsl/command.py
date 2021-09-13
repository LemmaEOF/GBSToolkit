from abc import ABC, ABCMeta, abstractmethod
from typing import Dict, List, Optional, Tuple, Union
from uuid import UUID

from .datatypes import ActorID, UnionArgument
from .enums import Direction
from .marshalling import JsonSafe
from .util import NameUtil

COMMAND_TYPES: Dict[str, "Command"] = {}  # Fills in automatically by subclassing Command! woooo

KEYWORDS: Dict[str, "Command"] = {}


class AutoRegister(ABCMeta):
    def __init__(cls, name, bases, clsdict):
        if len(cls.mro()) == 4 and "name" in clsdict and "keyword" in clsdict:
            COMMAND_TYPES[cls.name()] = cls
            KEYWORDS[cls.keyword()] = cls
        super(AutoRegister, cls).__init__(name, bases, clsdict)

    @staticmethod
    def name() -> str:
        pass

    @staticmethod
    def keyword() -> str:
        pass


class Command(ABC, metaclass=AutoRegister):
    @staticmethod
    @abstractmethod
    def name() -> str:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def keyword() -> str:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return None

    @classmethod
    @abstractmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return NotImplemented


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        return None, [names.actor_for_id(args["actorId"])]

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(arguments[0])}


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        return None, [names.actor_for_id(args["actorId"])]

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(arguments[0])}


class ActorEmoteCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_EMOTE"

    @staticmethod
    def keyword() -> str:
        return "emote"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "emoteId": int}

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        return None, [names.actor_for_id(args["actorId"]), args["emoteId"]]

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(arguments[0]), "emoteId": int(arguments[1])}


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        return None, [names.actor_for_id(args["actorId"]), args["direction"]]

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(arguments[0]), "direction": arguments[1]}


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        return None, [names.actor_for_id(args["actorId"]), args["vectorX"], args["vectorY"]]

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"actorId": names.id_for_actor(arguments[0]), "vectorX": arguments[1], "vectorY": arguments[2]}


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


class ActorInvokeCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_INVOKE"

    @staticmethod
    def keyword() -> str:
        return "invokeScript"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


class ActorMoveRelativeCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_MOVE_RELATIVE"

    @staticmethod
    def keyword() -> str:
        return "moveBy"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "x": int, "y": int}  # x and y range -31 to 31

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


class ActorMoveToCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_MOVE_TO"

    @staticmethod
    def keyword() -> str:
        return "moveTo"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "x": UnionArgument[int], "y": UnionArgument[int]}  # x 0-30, y 0-31

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


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

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass


class TextDialogueCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_TEXT"

    @staticmethod
    def keyword() -> str:
        return "say"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"text": Union[str, List[str]], "avatarId": Optional[UUID]}

    @classmethod
    def format(cls, args: Dict[str, JsonSafe], names: NameUtil) -> Tuple[Optional[Dict[str, JsonSafe]], Optional[List[JsonSafe]]]:
        pass

    @staticmethod
    def parse(properties: Optional[Dict[str, JsonSafe]], arguments: Optional[List[JsonSafe]], names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        pass
