from dataclasses import dataclass
from typing import Dict, Generic, TypeVar, Union
from uuid import UUID

from .enums import ActorProperty, Direction
from .marshalling import JsonSafe, serialize, Serializable


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
class NamedKey(Serializable):
    id: str  # I'd love this to be a number but thanks to custom event var names it can't be weirdly
    name: str

    def serialize(self) -> JsonSafe:
        return {"id": self.id, "name": self.name}

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "NamedKey":
        return NamedKey(
            id=obj["id"],
            name=obj["name"]
        )


@dataclass
class OwnedProperty(Serializable):
    actor: ActorID
    property: ActorProperty

    def serialize(self) -> JsonSafe:
        return serialize(self.actor + "." + serialize(self.property))

    @staticmethod
    def deserialize(prop: str) -> "OwnedProperty":
        split = prop.split(':')
        return OwnedProperty(
            actor=ActorID.deserialize(split[0]),
            property=ActorProperty.deserialize(split[1])
        )


T = TypeVar("T", int, Serializable)


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
        if type == "property":
            value = OwnedProperty.deserialize(obj["value"])
        elif type == "variable":
            value = str(obj["value"])  # TODO: deserialization context for defined variables? JSON doesn't care
        elif type == "direction":
            value = Direction.deserialize(obj["value"])
        elif type == "number":
            value = int(obj["value"])
        else:
            raise ValueError("Unexpected type `" + type + "` for union argument! Please report this so I can fix it!")
        return UnionArgument(
            type=type,
            value=value
        )
