from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from .datatypes import ActorID, UnionArgument, NamedKey
from .enums import Direction
from .marshalling import JsonSafe

COMMAND_TYPES = {}  # Fills in automatically by subclassing Command! woooo


class AutoRegister(ABCMeta):
    def __init__(cls, name, bases, clsdict):
        if len(cls.mro()) == 4 and "name" in clsdict:
            COMMAND_TYPES[cls.name()] = cls
        super(AutoRegister, cls).__init__(name, bases, clsdict)


class Command(ABC, metaclass=AutoRegister):
    @staticmethod
    @abstractmethod
    def name() -> str:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def children_names() -> Optional[List[str]]:
        return None

    @staticmethod
    @abstractmethod
    def format(args: Optional[Dict[str, Any]]) -> str:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        return NotImplemented


class ActorCollisionsDisableCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_COLLISIONS_DISABLE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorCollisionsEnableCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_COLLISIONS_ENABLE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorEmoteCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_EMOTE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "emoteId": int}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorGetDirectionCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_GET_DIRECTION"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "direction": str}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorGetPositionCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_GET_POSITION"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "vectorX": str, "VectorY": str}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorHideCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_HIDE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorInvokeCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_INVOKE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorMoveRelativeCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_MOVE_RELATIVE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "x": int, "y": int}  # x and y range -31 to 31

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorMoveToCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_MOVE_TO"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "x": UnionArgument[int], "y": UnionArgument[int]}  # x 0-30, y 0-31

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorPushCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_PUSH"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"continue": bool}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorSetAnimateCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_ANIMATE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "animate": bool}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorSetAnimationSpeedCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_ANIMATION_SPEED"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "animSpeed": Union[None, int]}  # range null and 0-4

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorSetDirectionCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_DIRECTION"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "direction": UnionArgument[Direction]}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorSetFrameCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_FRAME"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "frame": UnionArgument[int]}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorSetMovementSpeedCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_MOVEMENT_SPEED"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "speed": int}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorSetPositionCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_POSITION"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "x": UnionArgument[int], "y": UnionArgument[int]}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorSetPositionRelativeCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_POSITION_RELATIVE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "x": int, "y": int}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorSetSpriteCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SET_SPRITE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID, "spriteSheetId": UUID}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorShowCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_SHOW"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class ActorStopUpdateScriptCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_STOP_UPDATE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass


class TextDialogueCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_TEXT"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"text": Union[str, List[str]], "avatarId": Optional[UUID]}

    @staticmethod
    def format(args: Optional[Dict[str, Any]], children: Optional[Dict[str, List["Event"]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Dict[str, JsonSafe]:
        pass
