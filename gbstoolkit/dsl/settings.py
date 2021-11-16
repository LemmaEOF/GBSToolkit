from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID

from kdl import Node

from .enums import Direction
from .marshalling import JsonSafe, serialize, Serializable
from .palette import PaletteID
from .util import NameUtil, map_nodes, prop_node


@dataclass
class Settings(Serializable):
    start_scene_id: Optional[UUID]
    player_sprite_sheet_id: UUID
    start_x: int
    start_y: int
    start_move_speed: int
    start_anim_speed: int
    start_direction: Direction
    show_collisions: bool
    show_connections: bool
    world_scroll_x: float
    world_scroll_y: float
    zoom: float
    custom_colors_enabled: bool
    custom_head: str  # TODO: anything important to check with this? it's an HTML string
    default_background_palette_ids: List[PaletteID]
    default_sprite_palette_id: PaletteID
    default_ui_palette_id: PaletteID
    player_palette_id: PaletteID
    navigator_split_sizes: List[int]
    show_navigator: bool
    custom_colors_white: str
    custom_colors_light: str
    custom_colors_dark: str
    custom_colors_black: str
    cart_type: str
    custom_controls_up: Optional[List[str]]
    custom_controls_down: Optional[List[str]]
    custom_controls_left: Optional[List[str]]
    custom_controls_right: Optional[List[str]]
    custom_controls_a: Optional[List[str]]
    custom_controls_b: Optional[List[str]]
    custom_controls_start: Optional[List[str]]
    custom_controls_select: Optional[List[str]]

    def serialize(self) -> JsonSafe:
        ret = {
            "startSceneId": serialize(self.start_scene_id) if self.start_scene_id is not None else "",
            "playerSpriteSheetId": serialize(self.player_sprite_sheet_id),
            "startX": self.start_x,
            "startY": self.start_y,
            "startMoveSpeed": self.start_move_speed,
            "startAnimSpeed": self.start_anim_speed,
            "startDirection": serialize(self.start_direction),
            "showCollisions": self.show_collisions,
            "showConnections": self.show_connections,
            "worldScrollX": self.world_scroll_x,
            "worldScrollY": self.world_scroll_y,
            "zoom": self.zoom,
            "customColorsEnabled": self.custom_colors_enabled,
            "customHead": self.custom_head,
            "defaultBackgroundPaletteIds": serialize(self.default_background_palette_ids),
            "defaultSpritePaletteId": serialize(self.default_sprite_palette_id),
            "defaultUIPaletteId": serialize(self.default_ui_palette_id),
            "playerPaletteId": serialize(self.player_palette_id),
            "navigatorSplitSizes": self.navigator_split_sizes,
            "showNavigator": self.show_navigator,
            "customColorsWhite": self.custom_colors_white,
            "customColorsLight": self.custom_colors_light,
            "customColorsDark": self.custom_colors_dark,
            "customColorsBlack": self.custom_colors_black,
            "cartType": self.cart_type,
        }
        if self.custom_controls_up is not None:
            ret["customControlsUp"] = self.custom_controls_up
        if self.custom_controls_down is not None:
            ret["customControlsDown"] = self.custom_controls_down
        if self.custom_controls_left is not None:
            ret["customControlsLeft"] = self.custom_controls_left
        if self.custom_controls_right is not None:
            ret["customControlsRight"] = self.custom_controls_right
        if self.custom_controls_a is not None:
            ret["customControlsA"] = self.custom_controls_a
        if self.custom_controls_b is not None:
            ret["customControlsB"] = self.custom_controls_b
        if self.custom_controls_start is not None:
            ret["customControlsStart"] = self.custom_controls_start
        if self.custom_controls_select is not None:
            ret["customControlsSelect"] = self.custom_controls_select
        return ret

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Settings":
        id_read = obj["defaultSpritePaletteId"]
        default_sprite_palette_id = UUID(id_read) if len(id_read) == 36 else id_read
        id_read = obj["defaultUIPaletteId"]
        default_ui_palette_id = UUID(id_read) if len(id_read) == 36 else id_read
        id_read = obj["playerPaletteId"]
        player_palette_id = UUID(id_read) if len(id_read) == 36 else id_read
        return Settings(
            start_scene_id=UUID(obj["startSceneId"]) if obj["startSceneId"] != "" else None,
            player_sprite_sheet_id=UUID(obj["playerSpriteSheetId"]),
            start_x=obj["startX"],
            start_y=obj["startY"],
            start_move_speed=obj["startMoveSpeed"],
            start_anim_speed=obj["startAnimSpeed"],
            start_direction=Direction.deserialize(obj["startDirection"]),
            show_collisions=obj["showCollisions"],
            show_connections=obj["showConnections"],
            world_scroll_x=obj["worldScrollX"],
            world_scroll_y=obj["worldScrollY"],
            zoom=obj["zoom"],
            custom_colors_enabled=obj["customColorsEnabled"],
            custom_head=obj["customHead"],
            default_background_palette_ids=[UUID(i) if len(i) == 36 else i for i in obj["defaultBackgroundPaletteIds"]],
            default_sprite_palette_id=default_sprite_palette_id,
            default_ui_palette_id=default_ui_palette_id,
            player_palette_id=player_palette_id,
            navigator_split_sizes=obj["navigatorSplitSizes"],
            show_navigator=obj["showNavigator"],
            custom_colors_white=obj["customColorsWhite"] if "customColorsWhite" in obj else "E8F8E0",
            custom_colors_light=obj["customColorsLight"] if "customColorsLight" in obj else "B0F088",
            custom_colors_dark=obj["customColorsDark"] if "customColorsDark" in obj else "509878",
            custom_colors_black=obj["customColorsBlack"] if "customColorsBlack" in obj else "202850",
            cart_type=obj["cartType"] if "cartType" in obj else "1B",
            custom_controls_up=obj["customControlsUp"] if "customControlsUp" in obj else None,
            custom_controls_down=obj["customControlsDown"] if "customControlsDown" in obj else None,
            custom_controls_left=obj["customControlsLeft"] if "customControlsLeft" in obj else None,
            custom_controls_right=obj["customControlsRight"] if "customControlsRight" in obj else None,
            custom_controls_a=obj["customControlsA"] if "customControlsA" in obj else None,
            custom_controls_b=obj["customControlsB"] if "customControlsB" in obj else None,
            custom_controls_start=obj["customControlsStart"] if "customControlsStart" in obj else None,
            custom_controls_select=obj["customControlsSelect"] if "customControlsSelect" in obj else None
        )

    def format(self, names: NameUtil) -> Node:
        nodes = [
            prop_node("startScene", names.scene_for_id(str(self.start_scene_id)) if self.start_scene_id is not None else None),
            prop_node("playerSpriteSheet", names.sprite_for_id(str(self.player_sprite_sheet_id))),
            prop_node("startX", self.start_x),
            prop_node("startY", self.start_y),
            prop_node("startMoveSpeed", self.start_move_speed),
            prop_node("startAnimSpeed", self.start_anim_speed),
            prop_node("startDirection", self.start_direction.serialize()),
            prop_node("customColorsEnabled", self.custom_colors_enabled),
            prop_node("customHead", self.custom_head),
            Node(name="defaultBackgroundPalettes", nodes=[
                prop_node(
                    "palette" + str(self.default_background_palette_ids.index(i)),
                    names.palette_for_id(str(i))
                ) for i in self.default_background_palette_ids
            ]),
            prop_node("defaultSpritePalette", names.palette_for_id(str(self.default_sprite_palette_id))),
            prop_node("defaultUIPalette", names.palette_for_id(str(self.default_ui_palette_id))),
            prop_node(
                "playerPalette",
                names.palette_for_id(str(self.player_palette_id)) if self.player_palette_id != "" else ""
            ),
            Node(name="customColors", nodes=[
                prop_node("white", self.custom_colors_white),
                prop_node("light", self.custom_colors_light),
                prop_node("dark", self.custom_colors_dark),
                prop_node("black", self.custom_colors_black)
            ]),
            prop_node("cartType", self.cart_type)
        ]
        custom_controls = []
        if self.custom_controls_up is not None:
            custom_controls.append(Node("up", args=self.custom_controls_up))
        if self.custom_controls_down is not None:
            custom_controls.append(Node("down", args=self.custom_controls_down))
        if self.custom_controls_left is not None:
            custom_controls.append(Node("left", args=self.custom_controls_left))
        if self.custom_controls_right is not None:
            custom_controls.append(Node("right", args=self.custom_controls_right))
        if self.custom_controls_a is not None:
            custom_controls.append(Node("a", args=self.custom_controls_a))
        if self.custom_controls_b is not None:
            custom_controls.append(Node("b", args=self.custom_controls_b))
        if self.custom_controls_start is not None:
            custom_controls.append(Node("start", args=self.custom_controls_start))
        if self.custom_controls_select is not None:
            custom_controls.append(Node("select", args=self.custom_controls_select))
        if len(custom_controls) > 0:
            nodes.append(Node("customControls", nodes=custom_controls))
        nodes.extend([
            prop_node("__showCollisions", self.show_collisions),
            prop_node("__showConnections", self.show_connections),
            prop_node("__worldScrollX", self.world_scroll_x),
            prop_node("__worldScrollY", self.world_scroll_y),
            prop_node("__zoom", self.zoom),
            Node(name="__navigatorSplitSizes", args=self.navigator_split_sizes),
            prop_node("__showNavigator", self.show_navigator),
        ])
        return Node(name="settings", nodes=nodes)

    @staticmethod
    def parse(settings: List[Node], names: NameUtil) -> "Settings":
        contents = map_nodes(settings, ignore=["customControls", "__navigatorSplitSizes"])
        custom_colors = contents["customColors"]
        custom_controls = {}
        cc_nodes = [i for i in settings if i.name == "customControls"]
        if len(cc_nodes) > 0:
            control_node = cc_nodes[-1]
            custom_controls = {i.name: i.args for i in control_node.nodes}
        split_sizes = [205, 205, 546]
        split_nodes = [i for i in settings if i.name == "__navigatorSplitSizes"]
        if len(split_nodes) > 0:
            split_sizes = split_nodes[-1].args
        return Settings(
            start_scene_id=UUID(names.id_for_scene(contents["startScene"])) if contents["startScene"] is not None else None,
            start_x=contents["startX"],
            start_y=contents["startY"],
            start_move_speed=contents["startMoveSpeed"],
            start_anim_speed=contents["startAnimSpeed"],
            start_direction=Direction.deserialize(contents["startDirection"]),
            player_sprite_sheet_id=UUID(names.id_for_sprite(contents["playerSpriteSheet"])),
            show_collisions=contents["__showCollisions"],
            show_connections=contents["__showConnections"],
            world_scroll_x=contents["__worldScrollX"],
            world_scroll_y=contents["__worldScrollY"],
            zoom=contents["__zoom"],
            custom_colors_enabled=contents["customColorsEnabled"],
            custom_head=contents["customHead"],
            default_background_palette_ids=[
                names.id_for_palette(i) for i in contents["defaultBackgroundPalettes"].values()  # TODO: safe sorting
            ],
            default_sprite_palette_id=names.id_for_palette(contents["defaultSpritePalette"]),
            default_ui_palette_id=names.id_for_palette(contents["defaultUIPalette"]),
            player_palette_id=names.id_for_palette(contents["playerPalette"])
            if contents["playerPalette"] != "" else "",
            navigator_split_sizes=split_sizes,
            show_navigator=contents["__showNavigator"],
            custom_colors_white=custom_colors["white"],
            custom_colors_light=custom_colors["light"],
            custom_colors_dark=custom_colors["dark"],
            custom_colors_black=custom_colors["black"],
            cart_type=contents["cartType"],
            custom_controls_up=custom_controls["up"] if "down" in custom_controls else None,
            custom_controls_down=custom_controls["down"] if "down" in custom_controls else None,
            custom_controls_left=custom_controls["left"] if "left" in custom_controls else None,
            custom_controls_right=custom_controls["right"] if "right" in custom_controls else None,
            custom_controls_a=custom_controls["a"] if "a" in custom_controls else None,
            custom_controls_b=custom_controls["b"] if "b" in custom_controls else None,
            custom_controls_start=custom_controls["start"] if "start" in custom_controls else None,
            custom_controls_select=custom_controls["select"] if "select" in custom_controls else None,
        )


@dataclass
class EngineFields(Serializable):
    fade_style: Optional[int]
    topdown_grid: Optional[int]
    plat_min_vel: Optional[int]
    plat_walk_vel: Optional[int]
    plat_run_vel: Optional[int]
    plat_walk_acc: Optional[int]
    plat_run_acc: Optional[int]
    plat_dec: Optional[int]
    plat_jump_vel: Optional[int]
    plat_grav: Optional[int]
    plat_hold_grav: Optional[int]
    plat_max_fall_vel: Optional[int]

    def serialize(self) -> JsonSafe:
        ret = {}
        if self.fade_style is not None:
            ret["fade_style"] = self.fade_style
        if self.topdown_grid is not None:
            ret["topdown_grid"] = self.topdown_grid
        if self.plat_min_vel is not None:
            ret["plat_min_vel"] = self.plat_min_vel
        if self.plat_walk_vel is not None:
            ret["plat_walk_vel"] = self.plat_walk_vel
        if self.plat_run_vel is not None:
            ret["plat_run_vel"] = self.plat_run_vel
        if self.plat_walk_acc is not None:
            ret["plat_walk_acc"] = self.plat_walk_acc
        if self.plat_run_acc is not None:
            ret["plat_run_acc"] = self.plat_run_acc
        if self.plat_dec is not None:
            ret["plat_dec"] = self.plat_dec
        if self.plat_jump_vel is not None:
            ret["plat_jump_vel"] = self.plat_jump_vel
        if self.plat_grav is not None:
            ret["plat_grav"] = self.plat_grav
        if self.plat_hold_grav is not None:
            ret["plat_hold_grav"] = self.plat_hold_grav
        if self.plat_max_fall_vel is not None:
            ret["plat_max_fall_vel"] = self.plat_max_fall_vel
        return ret

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "EngineFields":
        return EngineFields(
            fade_style=obj["fade_style"] if "fade_style" in obj else None,
            topdown_grid=obj["topdown_grid"] if "topdown_grid" in obj else None,
            plat_min_vel=obj["plat_min_vel"] if "plat_min_vel" in obj else None,
            plat_walk_vel=obj["plat_walk_vel"] if "plat_walk_vel" in obj else None,
            plat_run_vel=obj["plat_run_vel"] if "plat_run_vel" in obj else None,
            plat_walk_acc=obj["plat_walk_acc"] if "plat_walk_acc" in obj else None,
            plat_run_acc=obj["plat_run_acc"] if "plat_run_acc" in obj else None,
            plat_dec=obj["plat_dec"] if "plat_dec" in obj else None,
            plat_jump_vel=obj["plat_jump_vel"] if "plat_jump_vel" in obj else None,
            plat_grav=obj["plat_grav"] if "plat_grav" in obj else None,
            plat_hold_grav=obj["plat_hold_grav"] if "plat_hold_grav" in obj else None,
            plat_max_fall_vel=obj["plat_max_fall_vel"] if "plat_max_fall_vel" in obj else None
        )

    def format(self) -> Node:
        nodes = []
        if self.fade_style is not None:
            nodes.append(
                Node(name="global", nodes=[prop_node("fadeStyle", "white" if self.fade_style == 1 else "black")])
            )
        if self.topdown_grid is not None:
            nodes.append(Node(name="topDown", nodes=[prop_node("gridSize", self.topdown_grid)]))
        plat_nodes = []
        if self.plat_min_vel is not None:
            plat_nodes.append(prop_node("minVelocity", self.plat_min_vel))
        if self.plat_walk_vel is not None:
            plat_nodes.append(prop_node("walkVelocity", self.plat_walk_vel))
        if self.plat_run_vel is not None:
            plat_nodes.append(prop_node("runVelocity", self.plat_run_vel))
        if self.plat_walk_acc is not None:
            plat_nodes.append(prop_node("walkAcceleration", self.plat_walk_acc))
        if self.plat_run_acc is not None:
            plat_nodes.append(prop_node("runAcceleration", self.plat_run_acc))
        if self.plat_dec is not None:
            plat_nodes.append(prop_node("deceleration", self.plat_dec))
        if self.plat_jump_vel is not None:
            plat_nodes.append(prop_node("jumpVelocity", self.plat_jump_vel))
        if self.plat_grav is not None:
            plat_nodes.append(prop_node("gravity", self.plat_grav))
        if self.plat_hold_grav is not None:
            plat_nodes.append(prop_node("jumpGravity", self.plat_hold_grav))
        if self.plat_max_fall_vel is not None:
            plat_nodes.append(prop_node("terminalVelocity", self.plat_max_fall_vel))
        if len(plat_nodes) > 0:
            nodes.append(Node(name="platformer", nodes=plat_nodes))
        return Node(name="engineFields", nodes=nodes)

    @staticmethod
    def parse(node: Node) -> "EngineFields":
        contents = map_nodes(node.nodes)
        global_vals = contents["global"] if "global" in contents else {}
        topdown_vals = contents["topDown"] if "topDown" in contents else {}
        platform_vals = contents["platformer"] if "platformer" in contents else {}
        return EngineFields(
            fade_style=(1 if global_vals["fadeStyle"] == "white" else 0) if "fadeStyle" in global_vals else None,
            topdown_grid=topdown_vals["gridSize"] if "gridSize" in topdown_vals else None,
            plat_min_vel=platform_vals["minVelocity"] if "minVelocity" in platform_vals else None,
            plat_walk_vel=platform_vals["walkVelocity"] if "walkVelocity" in platform_vals else None,
            plat_run_vel=platform_vals["runVelocity"] if "runVelocity" in platform_vals else None,
            plat_walk_acc=platform_vals["walkAcceleration"] if "walkAcceleration" in platform_vals else None,
            plat_run_acc=platform_vals["runAcceleration"] if "runAcceleration" in platform_vals else None,
            plat_dec=platform_vals["deceleration"] if "deceleration" in platform_vals else None,
            plat_jump_vel=platform_vals["jumpVelocity"] if "jumpVelocity" in platform_vals else None,
            plat_grav=platform_vals["gravity"] if "gravity" in platform_vals else None,
            plat_hold_grav=platform_vals["jumpGravity"] if "jumpGravity" in platform_vals else None,
            plat_max_fall_vel=platform_vals["terminalVelocity"] if "terminalVelocity" in platform_vals else None
        )
