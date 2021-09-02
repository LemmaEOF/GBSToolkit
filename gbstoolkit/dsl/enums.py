from enum import Enum

from marshalling import JsonSafe, Serializable


class SerializableEnum(Enum, Serializable):

    def serialize(self) -> JsonSafe:
        return self.value


class Direction(SerializableEnum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @staticmethod
    def deserialize(obj: str) -> "Direction":
        return Direction.__members__[obj]


class MovementType(SerializableEnum):
    STATIC = "static"
    RANDOM_WALK = "randomWalk"
    FACE_INTERACTION = "faceInteraction"

    @staticmethod
    def deserialize(obj: str) -> "MovementType":
        return MovementType.__members__[obj]


class SceneType(SerializableEnum):
    POINT_AND_CLICK = "POINTNCLICK"
    PLATFORMING = "PLATFORM"
    SHOOT_EM_UP = "SHMUP"
    TOP_DOWN = "TOPDOWN"

    @staticmethod
    def deserialize(obj: str) -> "SceneType":
        return SceneType.__members__[obj]


class SpriteSheetType(SerializableEnum):
    STATIC = "static"
    ANIMATED = "animated"
    ACTOR_ANIMATED = "actor_animated"

    @staticmethod
    def deserialize(obj: str) -> "SpriteSheetType":
        return SpriteSheetType.__members__[obj]


class SpriteType(SerializableEnum):
    STATIC = "static"
    ACTOR = "actor"

    @staticmethod
    def deserialize(obj: str) -> "SpriteType":
        return SpriteType.__members__[obj]
