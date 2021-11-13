from collections import OrderedDict
from typing import Dict, List, Optional
from uuid import UUID

from .cmd_base import Command
from ..datatypes import ActorID, UnionArgument
from ..enums import Direction, OverlayColor, SoundEffectType
from ..marshalling import JsonSafe
from ..palette import PaletteID
from ..util import NameUtil, NodeData


class CallCustomEventCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_CALL_CUSTOM_EVENT"

    @staticmethod
    def keyword() -> str:
        return "call"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"customEventId": UUID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        if len(args) > 2:
            props = OrderedDict()
            for k, v in args.items():
                if "variable" in k:
                    props["var" + k[10:-2]] = "$" + v + "$"
                elif "actor" in k:
                    props["actor" + k[7:-2]] = names.actor_for_id(v)
        else:
            props = OrderedDict()
        return NodeData(props, [names.custom_event_for_id(args["customEventId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {
            "customEventId": names.id_for_custom_event(data.args[0]),
            "__name": names.raw_custom_event_name(data.args[0])
        }
        if data.props is not None:
            for k, v in data.props.items():
                if k.startswith("var"):
                    ret["$variable[" + k[3:] + "]$"] = v[1:-1]
                elif k.startswith("actor"):
                    ret["$actor[" + k[5:] + "]$"] = names.id_for_actor(v)
        return ret


class CommentCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_COMMENT"

    @staticmethod
    def keyword() -> str:
        return "note"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"text": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [args["text"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"text": data.args[0]}


class DataClearCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_DATA_CLEAR"

    @staticmethod
    def keyword() -> str:
        return "clearSave"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class DataLoadCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_LOAD_DATA"

    @staticmethod
    def keyword() -> str:
        return "loadSave"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class DataSaveCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SAVE_DATA"

    @staticmethod
    def keyword() -> str:
        return "createSave"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class LaunchProjectileCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_LAUNCH_PROJECTILE"

    @staticmethod
    def keyword() -> str:
        return "launchProjectile"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {
            "spriteSheetId": UUID,
            "actorId": ActorID,
            "direction": UnionArgument[Direction],
            "speed": int,
            "collisionGroup": str,
            "collisionMask": List[str]
        }

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({
            "speed": args["speed"],
            "collision": args["collisionGroup"]
        })
        for i in args["collisionMask"]:
            props["collide" + i.capitalize()] = True
        return NodeData(props, [
            names.actor_for_id(args["actorId"]),
            names.sprite_for_id(args["spriteSheetId"]),
            UnionArgument.format(args["direction"], names)
        ])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        collision_mask = []
        if "collidePlayer" in data.props:
            collision_mask.append("player")
        if "collide1" in data.props:
            collision_mask.append("1")
        if "collide2" in data.props:
            collision_mask.append("2")
        if "collide3" in data.props:
            collision_mask.append("3")
        return {
            "spriteSheetId": names.id_for_sprite(data.args[1]),
            "actorId": names.id_for_actor(data.args[0]),
            "direction": UnionArgument.parse(data.args[2], names, ("direction", Direction)),
            "speed": data.props["speed"],
            "collisionGroup": data.props["collision"],
            "collisionMask": collision_mask
        }


class MusicPlayCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_MUSIC_PLAY"

    @staticmethod
    def keyword() -> str:
        return "playMusic"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"musicId": UUID, "loop": bool}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"loop": args["loop"]}), [names.song_for_id(args["musicId"])])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"musicId": names.id_for_song(data.args[0]), "loop": data.props["loop"]}


class MusicStopCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_MUSIC_STOP"

    @staticmethod
    def keyword() -> str:
        return "stopMusic"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class OverlayHideCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_OVERLAY_HIDE"

    @staticmethod
    def keyword() -> str:
        return "hideOverlay"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class OverlayMoveToCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_OVERLAY_MOVE_TO"

    @staticmethod
    def keyword() -> str:
        return "moveOverlay"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"x": int, "y": int, "speed": str}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"speed": args["speed"]}), [args["x"], args["y"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"x": data.args[0], "y": data.args[1], "speed": data.props["speed"]}


class OverlayShowCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_OVERLAY_SHOW"

    @staticmethod
    def keyword() -> str:
        return "showOverlay"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"color": OverlayColor, "x": int, "y": int}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict({"color": args["color"]}), [args["x"], args["y"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "x": data.args[0],
            "y": data.args[1],
            "color": data.props["color"] if "color" in data.props else "black"
        }


class PaletteSetBackgroundCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_PALETTE_SET_BACKGROUND"

    @staticmethod
    def keyword() -> str:
        return "setBackgroundPalette"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {
            "palette0": PaletteID,
            "palette1": PaletteID,
            "palette2": PaletteID,
            "palette3": PaletteID,
            "palette4": PaletteID,
            "palette5": PaletteID
        }

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(),
                        [names.palette_for_id(args["palette" + str(i)]) if args["palette" + str(i)] != "" else ""
                         for i in range(6)]
                        )
        # kept around in case this list comp doesn't work
        # return NodeData(OrderedDict(), [
        #     names.palette_for_id(args["palette0"]) if args["palette0"] != "" else "",
        #     names.palette_for_id(args["palette1"]) if args["palette1"] != "" else "",
        #     names.palette_for_id(args["palette2"]) if args["palette2"] != "" else "",
        #     names.palette_for_id(args["palette3"]) if args["palette3"] != "" else "",
        #     names.palette_for_id(args["palette4"]) if args["palette4"] != "" else "",
        #     names.palette_for_id(args["palette5"]) if args["palette5"] != "" else ""
        # ])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {"palette" + str(i): names.id_for_palette(data.args[i]) if data.args[i] != "" else "" for i in range(6)}
        # kept around in case this dict comp doesn't work
        # return {
        #     "palette0": names.id_for_palette(data.args[0]) if data.args[0] != "" else "",
        #     "palette1": names.id_for_palette(data.args[1]) if data.args[1] != "" else "",
        #     "palette2": names.id_for_palette(data.args[2]) if data.args[2] != "" else "",
        #     "palette3": names.id_for_palette(data.args[3]) if data.args[3] != "" else "",
        #     "palette4": names.id_for_palette(data.args[4]) if data.args[4] != "" else "",
        #     "palette5": names.id_for_palette(data.args[5]) if data.args[5] != "" else "",
        # }


class PaletteSetUICommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_PALETTE_SET_UI"

    @staticmethod
    def keyword() -> str:
        return "setUIPalette"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"palette": PaletteID}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [names.palette_for_id(args["palette"]) if args["palette"] != "" else ""])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return {
            "palette": names.id_for_palette(data.args[0]) if data.args[0] != "" else ""
        }


class ScriptStopCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_STOP"

    @staticmethod
    def keyword() -> str:
        return "stop"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return None

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        return NodeData(OrderedDict(), [])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        return None


class SoundPlayEffectCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_SOUND_PLAY_EFFECT"

    @staticmethod
    def keyword() -> str:
        return "playSound"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {"type": SoundEffectType, "duration": int, "wait": bool}

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict()
        if args["type"] == "beep":
            props["pitch"] = args["pitch"]
        elif args["type"] == "tone":
            props["tone"] = args["tone"]
        props["wait"] = args["wait"]
        return NodeData(props, [args["type"], args["duration"]])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        ret = {"type": data.args[0]}
        if ret["type"] == "beep":
            ret["pitch"] = data.props["pitch"]
        elif ret["type"] == "tone":
            ret["frequency"] = data.props["frequency"]
        ret["duration"] = data.args[1]
        ret["wait"] = data.props["wait"]
        return ret


class WeaponAttackCommand(Command):
    @staticmethod
    def name() -> str:
        return "EVENT_WEAPON_ATTACK"

    @staticmethod
    def keyword() -> str:
        return "useWeapon"

    @staticmethod
    def required_args() -> Optional[Dict[str, type]]:
        return {
            "spriteSheetId": UUID,
            "actorId": ActorID,
            "offset": int,
            "collisionGroup": str,
            "collisionMask": List[str]
        }

    @staticmethod
    def format(args: Optional[Dict[str, JsonSafe]], names: NameUtil) -> NodeData:
        props = OrderedDict({
            "offset": args["offset"]
        })
        for i in args["collisionMask"]:
            props["collide" + i.capitalize()] = True
        return NodeData(props, [
            names.actor_for_id(args["actorId"]),
            names.sprite_for_id(args["spriteSheetId"]),
            UnionArgument.format(args["direction"], names)
        ])

    @staticmethod
    def parse(data: NodeData, names: NameUtil) -> Optional[Dict[str, JsonSafe]]:
        collision_mask = []
        if "collidePlayer" in data.props:
            collision_mask.append("player")
        if "collide1" in data.props:
            collision_mask.append("1")
        if "collide2" in data.props:
            collision_mask.append("2")
        if "collide3" in data.props:
            collision_mask.append("3")
        return {
            "spriteSheetId": names.id_for_sprite(data.args[1]),
            "actorId": names.id_for_actor(data.args[0]),
            "direction": UnionArgument.parse(data.args[2], names, ("direction", Direction)),
            "offset": data.props["offset"],
            "collisionMask": collision_mask
        }
