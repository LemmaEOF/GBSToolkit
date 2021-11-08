"""
Additional types to cover for multiple possible values in event arguments, plus serialization tools.
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, Dict, List, Union
from uuid import UUID

from .enums import SerializableEnum

JsonSafe = Union[Dict[str, "JsonSafe"], List["JsonSafe"], str, int, float, bool, None]


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> JsonSafe:
        return NotImplemented


def serialize(obj: Any) -> JsonSafe:
    if type(obj) == int or type(obj) == bool or type(obj) == str or obj is None:
        # Already safe! Go on ahead!
        return obj
    if type(obj) == float:
        # Check if we can truncate floats!
        if obj.is_integer():
            return int(obj)
        return obj
    if type(obj) == UUID:
        # A UUID! We special-case these because they're damn well everywhere in GB Studio
        return str(obj)
    elif type(obj) == dict:
        # A dict! Might not be safe yet. Map it to be sure!
        return {str(k): serialize(v) for k, v in obj.items()}
    elif type(obj) == list:
        # A list! Might not be safe yet. Map it to be sure!
        return[serialize(i) for i in obj]
    elif isinstance(obj, Serializable):
        # We know it's serializable! Serialize it!
        return obj.serialize()
    elif isinstance(obj, SerializableEnum):
        # We know it's serializable as an enum! Serialize it!
        return obj.serialize()
    elif isinstance(obj, OrderedDict):
        return {str(k): serialize(v) for k, v in obj.items()}
    else:
        # We don't know how to serialize this! Give up because we don't really care about full capabilities!
        raise ValueError("Attempted to serialize un-serializable type " + str(type(obj)))
