from pathlib import Path
from mod_generator.modules import Logger
from mod_generator.get_mask import get_mask
from PIL import Image

SUPPORTED_FILETYPES: list[str] = [".png"]

def generate_user_selected_files(
    base_directory: Path,
    colors: list[str],
    angle: int,
    user_selected_files: list[dict[str, Path | list[str]]]
) -> None:
    for filepath in user_selected_files:
        source: Path = filepath["source"]
        target: list[str] = filepath["target"]

        if not source.is_file():
            Logger.warning(f"File not found: {source.name}", prefix="mod_generator.generate_user_selected_files()")
            continue

        if source.suffix.lower() not in SUPPORTED_FILETYPES:
            Logger.warning(f"Cannot generate file: {source.name}! Only .png files are supported", prefix="mod_generator.generate_user_selected_files()")
            continue

        target_path: Path = Path(base_directory, *target)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(source, formats=("PNG",)) as image:
            image = image.convert("RGBA")
            r, g, b, a = image.split()

        modded_icon = get_mask(colors, angle, image.size)
        modded_icon.putalpha(a)
        modded_icon.save(target_path, format="PNG", optimize=False)
