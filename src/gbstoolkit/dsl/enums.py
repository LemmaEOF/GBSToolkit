from enum import Enum


class SerializableEnum(Enum):

    def serialize(self) -> str:
        return self.value


class ActorProperty(SerializableEnum):
    X_POS = "xpos"
    Y_POS = "ypos"
    DIRECTION = "direction"
    MOVE_SPEED = "moveSpeed"
    ANIM_SPEED = "animSpeed"
    FRAME = "frame"

    @staticmethod
    def deserialize(obj: str) -> "ActorProperty":
        return ActorProperty(obj)


class Direction(SerializableEnum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @staticmethod
    def deserialize(obj: str) -> "Direction":
        return Direction(obj)


class MovementType(SerializableEnum):
    STATIC = "static"
    RANDOM_WALK = "randomWalk"
    FACE_INTERACTION = "faceInteraction"

    @staticmethod
    def deserialize(obj: str) -> "MovementType":
        return MovementType(obj)


class SceneType(SerializableEnum):  # TODO: swap names in V3!
    TOP_DOWN = "0"  # "TOPDOWN"
    PLATFORMING = "1"  # "PLATFORM"
    ADVENTURE = "2" # "ADVENTURE"
    SHOOT_EM_UP = "3"  # "SHMUP"
    POINT_AND_CLICK = "4"  # "POINTNCLICK"
    # LOGO = "LOGO"

    @staticmethod
    def deserialize(obj: str) -> "SceneType":
        return SceneType(obj)


class SpriteSheetType(SerializableEnum):
    STATIC = "static"
    ANIMATED = "animated"
    ACTOR = "actor"
    ACTOR_ANIMATED = "actor_animated"

    @staticmethod
    def deserialize(obj: str) -> "SpriteSheetType":
        return SpriteSheetType(obj)


class SpriteType(SerializableEnum):
    STATIC = "static"
    ACTOR = "actor"

    @staticmethod
    def deserialize(obj: str) -> "SpriteType":
        return SpriteType(obj)
