from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID

from event import Event
from marshalling import ActorID


class Command(ABC):
    @staticmethod
    @abstractmethod
    def name() -> str:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def has_children() -> bool:
        return False

    @abstractmethod
    def format(self, args: Optional[Dict[str, Any]], children: Optional[Dict[str, List[Event]]]) -> str:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def parse(text: str) -> Event:
        return NotImplemented


class ActorCollisionsDisableCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_COLLISIONS_DISABLE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    def format(self, args: Optional[Dict[str, Any]], children: Optional[Dict[str, List[Event]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Event:
        pass


class ActorCollisionsEnableCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_ACTOR_COLLISIONS_ENABLE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"actorId": ActorID}

    def format(self, args: Optional[Dict[str, Any]], children: Optional[Dict[str, List[Event]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Event:
        pass


class ActorEmoteCommand(Command):

    @staticmethod
    def name() -> str:
        "EVENT_ACTOR_EMOTE"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"id": ActorID, "emoteId": int}

    def format(self, args: Optional[Dict[str, Any]], children: Optional[Dict[str, List[Event]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Event:
        pass


class TextDialogueCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_TEXT"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"text": str, "avatarId": Optional[UUID]}

    def format(self, args: Optional[Dict[str, Any]], children: Optional[Dict[str, List[Event]]]) -> str:
        pass

    @staticmethod
    def parse(text: str) -> Event:
        pass


COMMAND_TYPES = {
    "EVENT_ACTOR_COLLISIONS_DISABLE": ActorCollisionsDisableCommand,
    "EVENT_ACTOR_COLLISIONS_ENABLE": ActorCollisionsEnableCommand,
    "EVENT_ACTOR_EMOTE": ActorEmoteCommand,
    "EVENT_TEXT": TextDialogueCommand
}