from dataclasses import dataclass
from typing import List
from uuid import UUID

from enums import Direction
from marshalling import JsonSafe, serialize, Serializable
from palette import PaletteID


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
