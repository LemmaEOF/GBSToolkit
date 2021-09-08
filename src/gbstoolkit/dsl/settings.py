from dataclasses import dataclass
from typing import Dict, List
from uuid import UUID

from .enums import Direction
from .marshalling import JsonSafe, serialize, Serializable
from .palette import PaletteID


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
