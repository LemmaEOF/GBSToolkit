from dataclasses import dataclass
from typing import Dict, List
from uuid import UUID

from kdl import Node

from .enums import Direction
from .marshalling import JsonSafe, serialize, Serializable
from .palette import PaletteID
from .util import NameUtil, map_nodes, prop_node


# TODO: customHead, showNavigator, navigatorSplitSizes, cartType, playerPaletteId
@dataclass
class Settings(Serializable):
    start_scene_id: UUID
    start_x: int
    start_y: int
    show_collisions: bool
    show_connections: bool
    world_scroll_x: float
    world_scroll_y: float
    zoom: float
    custom_colors_enabled: bool
    default_background_palette_ids: List[PaletteID]
    default_sprite_palette_id: PaletteID
    default_ui_palette_id: PaletteID
    custom_colors_white: str
    custom_colors_light: str
    custom_colors_dark: str
    custom_colors_black: str
    start_direction: Direction
    player_sprite_sheet_id: UUID

    def serialize(self) -> JsonSafe:
        return {
            "startSceneId": serialize(self.start_scene_id),
            "startX": self.start_x,
            "startY": self.start_y,
            "showCollisions": self.show_collisions,
            "showConnections": self.show_connections,
            "worldScrollX": self.world_scroll_x,
            "worldScrollY": self.world_scroll_y,
            "zoom": self.zoom,
            "customColorsEnabled": self.custom_colors_enabled,
            "defaultBackgroundPaletteIds": serialize(self.default_background_palette_ids),
            "defaultSpritePaletteId": serialize(self.default_sprite_palette_id),
            "defaultUIPaletteId": serialize(self.default_ui_palette_id),
            "customColorsWhite": self.custom_colors_white,
            "customColorsLight": self.custom_colors_light,
            "customColorsDark": self.custom_colors_dark,
            "customColorsBlack": self.custom_colors_black,
            "startDirection": serialize(self.start_direction),
            "playerSpriteSheetId": serialize(self.player_sprite_sheet_id)
        }

    @staticmethod
    def deserialize(obj: Dict[str, JsonSafe]) -> "Settings":
        id_read = obj["defaultSpritePaletteId"]
        default_sprite_palette_id = UUID(id_read) if len(id_read) == 36 else id_read
        id_read = obj["defaultUIPaletteId"]
        default_ui_palette_id = UUID(id_read) if len(id_read) == 36 else id_read
        return Settings(
            start_scene_id=UUID(obj["startSceneId"]),
            start_x=obj["startX"],
            start_y=obj["startY"],
            show_collisions=obj["showCollisions"],
            show_connections=obj["showConnections"],
            world_scroll_x=obj["worldScrollX"],
            world_scroll_y=obj["worldScrollY"],
            zoom=obj["zoom"],
            custom_colors_enabled=obj["customColorsEnabled"],
            default_background_palette_ids=[UUID(i) if len(i) == 36 else i for i in obj["defaultBackgroundPaletteIds"]],
            default_sprite_palette_id=default_sprite_palette_id,
            default_ui_palette_id=default_ui_palette_id,
            custom_colors_white=obj["customColorsWhite"],
            custom_colors_light=obj["customColorsLight"],
            custom_colors_dark=obj["customColorsDark"],
            custom_colors_black=obj["customColorsBlack"],
            start_direction=Direction.deserialize(obj["startDirection"]),
            player_sprite_sheet_id=UUID(obj["playerSpriteSheetId"])
        )

    def format(self, names: NameUtil) -> Node:
        children = [
            prop_node("startScene", names.scene_for_id(str(self.start_scene_id))),
            prop_node("startX", self.start_x),
            prop_node("startY", self.start_y),
            prop_node("startDirection", self.start_direction.serialize()),
            prop_node("playerSpriteSheet", names.sprite_for_id(str(self.player_sprite_sheet_id))),
            prop_node("showCollisions", self.show_collisions),
            prop_node("showConnections", self.show_connections),
            prop_node("worldScrollX", self.world_scroll_x),
            prop_node("worldScrollY", self.world_scroll_y),
            prop_node("zoom", self.zoom),
            prop_node("customColorsEnabled", self.custom_colors_enabled),
            Node("defaultBackgroundPalettes", None, None, [
                prop_node(
                    "palette" + str(self.default_background_palette_ids.index(i)),
                    names.palette_for_id(str(i))
                ) for i in self.default_background_palette_ids
            ]),
            prop_node("defaultSpritePalette", names.palette_for_id(str(self.default_sprite_palette_id))),
            prop_node("defaultUIPalette", names.palette_for_id(str(self.default_ui_palette_id))),
            Node("customColors", None, None, [
                prop_node("white", self.custom_colors_white),
                prop_node("light", self.custom_colors_light),
                prop_node("dark", self.custom_colors_dark),
                prop_node("black", self.custom_colors_black)
            ])
        ]
        return Node("settings", None, None, children)

    @staticmethod
    def parse(settings: List[Node], names: NameUtil) -> "Settings":
        contents = map_nodes(settings)
        custom_colors = contents["customColors"]
        return Settings(
            start_scene_id=UUID(names.id_for_scene(contents["startScene"])),
            start_x=contents["startX"],
            start_y=contents["startY"],
            start_direction=Direction.deserialize(contents["startDirection"]),
            player_sprite_sheet_id=UUID(names.id_for_sprite(contents["playerSpriteSheet"])),
            show_collisions=contents["showCollisions"],
            show_connections=contents["showConnections"],
            world_scroll_x=contents["worldScrollX"],
            world_scroll_y=contents["worldScrollY"],
            zoom=contents["zoom"],
            custom_colors_enabled=contents["customColorsEnabled"],
            default_background_palette_ids=[
                names.id_for_palette(i) for i in contents["defaultBackgroundPalettes"].values()  # TODO: safe sorting
            ],
            default_sprite_palette_id=names.id_for_palette(contents["defaultSpritePalette"]),
            default_ui_palette_id=names.id_for_palette(contents["defaultUIPalette"]),
            custom_colors_white=custom_colors["white"],
            custom_colors_light=custom_colors["light"],
            custom_colors_dark=custom_colors["dark"],
            custom_colors_black=custom_colors["black"]
        )