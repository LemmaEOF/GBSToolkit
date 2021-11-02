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

class AutoMovementType(SerializableEnum):
    STATIC = "static"
    RANDOM_WALK = "randomWalk"
    FACE_INTERACTION = "faceInteraction"

    @staticmethod
    def deserialize(obj: str) -> "AutoMovementType":
        return AutoMovementType(obj)


class Direction(SerializableEnum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @staticmethod
    def deserialize(obj: str) -> "Direction":
        return Direction(obj)


class MoveType(SerializableEnum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    DIAGONAL = "diagonal"

    @staticmethod
    def deserialize(obj: str) -> "MoveType":
        return MoveType(obj)


class OverlayColor(SerializableEnum):
    BLACK = ("black", 0)
    WHITE = ("white", 1)

    def serialize(self) -> int:
        return self.value[1]

    @staticmethod
    def deserialize(obj: int) -> "OverlayColor":
        return OverlayColor.BLACK if obj == 0 else OverlayColor.WHITE

    @staticmethod
    def format(obj: int) -> str:
        return "black" if obj == 0 else "white"

    @staticmethod
    def parse(obj: str) -> int:
        return 0 if obj == "black" else "white"


class RelativeActorPosition(SerializableEnum):
    ABOVE = ("up", "above")
    BELOW = ("down", "below")
    LEFT_OF = ("left", "left_of")
    RIGHT_OF = ("right", "right_of")

    def serialize(self) -> str:
        return self.value[0]

    @staticmethod
    def deserialize(obj: str) -> "RelativeActorPosition":
        if obj == "up":
            return RelativeActorPosition.ABOVE
        if obj == "down":
            return RelativeActorPosition.BELOW
        if obj == "left":
            return RelativeActorPosition.LEFT_OF
        if obj == "right":
            return RelativeActorPosition.RIGHT_OF
        raise KeyError("Couldn't find relative actor position for value '" + obj + "'")

    @staticmethod
    def format(obj: str) -> str:
        pos = RelativeActorPosition.deserialize(obj)
        return pos.value[1]

    @staticmethod
    def parse(obj: str) -> str:
        if obj == "above":
            return RelativeActorPosition.ABOVE.serialize()
        if obj == "below":
            return RelativeActorPosition.BELOW.serialize()
        if obj == "left_of":
            return RelativeActorPosition.LEFT_OF.serialize()
        if obj == "right_of":
            return RelativeActorPosition.RIGHT_OF.serialize()
        raise KeyError("Couldn't find relative actor position for value '" + obj + "'")


class SceneType(SerializableEnum):  # TODO: swap names in V3!
    TOP_DOWN = "0"  # "TOPDOWN"
    PLATFORMING = "1"  # "PLATFORM"
    ADVENTURE = "2"  # "ADVENTURE"
    SHOOT_EM_UP = "3"  # "SHMUP"
    POINT_AND_CLICK = "4"  # "POINTNCLICK"
    # LOGO = "LOGO"

    @staticmethod
    def deserialize(obj: str) -> "SceneType":
        return SceneType(obj)


class SoundEffectType(SerializableEnum):
    BEEP = "beep",
    TONE = "tone",
    CRASH = "crash"

    @staticmethod
    def deserialize(obj: str) -> "SoundEffectType":
        return SoundEffectType(obj)


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
