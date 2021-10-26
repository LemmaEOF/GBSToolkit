from dataclasses import dataclass
from typing import Dict, Generic, Tuple, Type, TypeVar, Union
from uuid import UUID

from .enums import ActorProperty, Direction, SerializableEnum
from .marshalling import JsonSafe, serialize, Serializable
from .util import NameUtil


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
class OwnedProperty(Serializable):
    actor: ActorID
    property: ActorProperty

    def serialize(self) -> JsonSafe:
        return self.actor.serialize() + ":" + self.property.serialize()

    @staticmethod
    def deserialize(prop: str) -> "OwnedProperty":
        split = prop.split(':')
        return OwnedProperty(
            actor=ActorID.deserialize(split[0]),
            property=ActorProperty.deserialize(split[1])
        )

    @staticmethod
    def format(obj: str, names: NameUtil) -> str:
        prop =  OwnedProperty.deserialize(obj)
        return names.actor_for_id(prop.actor.serialize()) + ":" + prop.property.serialize()

    @staticmethod
    def parse(obj: str, names: NameUtil) -> str:
        split = obj.split(':')
        return names.id_for_actor(split[0]) + ":" + split[1]


T = TypeVar("T", int, Serializable, SerializableEnum)


@dataclass
class UnionArgument(Serializable, Generic[T]):
    type: str
    value: Union[T, str, OwnedProperty]  # Raw value, var, or owned property (human-readable var name doesn't matter)

    def serialize(self) -> JsonSafe:
        return {
            "type": self.type,
            "value": serialize(self.value)
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "UnionArgument":
        type = obj["type"]
        if type == "property":  # "84a068f6-ccd4-4b63-a78f-d4787ed25d87:direction"
            value = OwnedProperty.deserialize(obj["value"])
        elif type == "variable":  # "$5$"
            value = str(obj["value"])
        elif type == "direction":  # "up", "down", "left", or "right"
            value = Direction.deserialize(obj["value"])
        elif type == "number":  # raw number
            value = int(obj["value"])
        else:
            raise ValueError("Unexpected type `" + type + "` for union argument! Please report this so I can fix it!")
        return UnionArgument(
            type=type,
            value=value
        )

    @staticmethod
    def format(obj: Dict[str, JsonSafe], names: NameUtil) -> Union[str, int]:
        if "type" not in obj:  # can happen (wheeee), just default to number bc that's Probably Safe
            return obj["value"]
        if obj["type"] == "variable":
            return "$" + obj["value"] + "$"
        elif obj["type"] == "property":
            return OwnedProperty.format(obj["value"], names)
        else:  # TODO: any other important conditions here?
            return obj["value"]

    @staticmethod
    def parse(obj: Union[str, int], names: NameUtil, arg: Tuple[str, Type[T]] = ("number", int)) -> Dict[str, JsonSafe]:
        if type(obj) == int or type(obj) == float:
            return {"type": "number", "value": int(obj)}
        else:
            if obj[0] == "$" and obj[-1] == "$":
                return {"type": "variable", "value": obj[1:-1]}
            elif ':' in obj:
                return {"type": "property", "value": OwnedProperty.parse(obj, names)}
            else:
                if arg[1] == int:
                    return {"type": arg[0], "value": int(obj)}
                else:
                    return {"type": arg[0], "value": arg[1].deserialize(obj).serialize()}
