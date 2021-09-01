"""
Additional types to cover for multiple possible values in event arguments, plus serialization tools.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from types import NoneType
from typing import Any, Dict, List, Union
from uuid import UUID

JsonSafe = Union[Dict[str, "JsonSafe"], List["JsonSafe"], str, int, float, bool]


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> JsonSafe:
        return NotImplemented


def serialize(obj: Any) -> JsonSafe:
    if type(obj) == int or type(obj) == float or type(obj) == bool or type(obj) == str or type(obj) == NoneType:
        # Already safe! Go on ahead!
        return obj
    if type(obj) == UUID:
        # A UUID! We special-case these because they're damn well everywhere in GB Studio
        return str(obj)
    elif type(obj) == dict:
        # A dict! Might not be safe yet. Map it to be sure!
        return {str(k): serialize(v) for k, v in obj}
    elif type(obj) == list:
        # A list! Might not be safe yet. Map it to be sure!
        return[serialize(i) for i in obj]
    elif isinstance(obj, Serializable):
        # We know it's serializable! Serialize it!
        return obj.serialize()
    else:
        # We don't know how to serialize this! Give up because we don't really care about full capabilities!
        raise ValueError("Attempted to serialize un-serializable type " + str(type(obj)))


@dataclass
class ActorID(Serializable):
    id: Union[UUID, int, str]

    def is_player(self) -> bool:
        return self.id == "player"

    def is_self(self) -> bool:
        return self.id == "$self$"

    def serialize(self) -> JsonSafe:
        return str(self.id)

    @staticmethod
    def deserialize(actorid: str) -> "ActorID":
        # trying Python's UUID value testing to check if it's a UUID
        uuidtest = actorid.strip('{}').replace('-', '')
        if actorid.isnumeric():
            return ActorID(int(actorid))
        elif len(uuidtest) == 32:
            return ActorID(UUID(actorid))
        elif actorid == "player" or actorid == "$self$":
            return ActorID(actorid)
        else:
            raise ValueError("Actor ID should be a UUID, integer ID, `player`, or `$self$`")


@dataclass
class Variable(Serializable):
    id: int
    name: str

    def serialize(self) -> JsonSafe:
        return {"id": str(self.id), "name": self.name}