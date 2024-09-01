import os

from typing import Final

THEME_NAME: Final[str] = "hush"

LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "WARNING")

COMMANDS_DIRECTORY: Final[str] = "utils/commands"

SRC_THEME_FILE: Final[str] = "hush/colors.toml"
SRC_VARIANTS_DIRECTORY: Final[str] = "hush/variants"

DIST_THEMES_DIRECTORY: Final[str] = "dist"
DIST_THEME_FILE_EXTENSION: Final[str] = ".toml"
