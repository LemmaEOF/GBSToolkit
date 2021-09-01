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


class MovementType(SerializableEnum):
    STATIC = "static"
    RANDOM_WALK = "randomWalk"
    FACE_INTERACTION = "faceInteraction"


class SceneType(SerializableEnum):
    POINT_AND_CLICK = "POINTNCLICK"
    PLATFORMING = "PLATFORM"
    SHOOT_EM_UP = "SHMUP"
    TOP_DOWN = "TOPDOWN"


class SpriteSheetType(SerializableEnum):
    STATIC = "static"
    ANIMATED = "animated"
    ACTOR_ANIMATED = "actor_animated"


class SpriteType(SerializableEnum):
    STATIC = "static"
    ACTOR = "actor"
