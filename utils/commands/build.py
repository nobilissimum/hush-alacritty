from os import scandir
from pathlib import Path

import toml

from utils.settings import (
    DIST_THEME_FILE_EXTENSION,
    DIST_THEMES_DIRECTORY,
    SRC_THEME_FILE,
    SRC_VARIANTS_DIRECTORY,
    THEME_NAME,
)


def create_theme_file(config: dict, name: str) -> dict:
    hex_length: int = 2

    ansi_white: str = config["ansi_white"]

    background: str = config["main"]
    background_hex: str = background[1:]
    background_hex_rgb: list[int] = [
        int(background_hex[i : i + hex_length], 16)
        for i in range(0, len(background_hex), 2)
    ]

    white: int = int("ff", 16)
    ansi_bright_black: str = "#" + "".join(
        [f"{int((bg_hex + white) / 2):x}" for bg_hex in background_hex_rgb],
    )

    ansi_colors: dict[str, str] = {
        "black": config["ansi_black"],
        "red": config["ansi_red"],
        "green": config["ansi_green"],
        "yellow": config["ansi_yellow"],
        "blue": config["ansi_blue"],
        "magenta": config["ansi_magenta"],
        "cyan": config["ansi_cyan"],
        "white": ansi_white,
    }

    dist_config: dict = {
        "colors": {
            "primary": {
                "background": background,
                "foreground": ansi_white,
            },
            "normal": ansi_colors,
            "bright": {
                **ansi_colors,
                "black": ansi_bright_black,
            },
        },
    }

    theme_dirpath: Path = Path(DIST_THEMES_DIRECTORY)
    theme_filepath: Path = (theme_dirpath / name).with_suffix(DIST_THEME_FILE_EXTENSION)
    if not theme_dirpath.exists():
        theme_dirpath.mkdir()

    with theme_filepath.open("w") as file:
        toml.dump(dist_config, file)

    return dist_config


def main() -> None:
    config: dict
    with Path(SRC_THEME_FILE).open() as file:
        config = toml.load(file)

    # Create base theme
    create_theme_file(config, THEME_NAME)

    # Create variant themes
    with scandir(SRC_VARIANTS_DIRECTORY) as directory_entries:
        for entry in directory_entries:
            if not entry.is_file():
                continue

            variant_path: Path = Path(entry)
            if variant_path.suffix != ".toml":
                continue

            variant_config: dict = {**config}
            with Path(entry.path).open() as file:
                variant_config.update(toml.load(file))
                create_theme_file(
                    variant_config,
                    f"{THEME_NAME}-{Path(entry.name).stem}",
                )


if __name__ == "__main__":
    main()
