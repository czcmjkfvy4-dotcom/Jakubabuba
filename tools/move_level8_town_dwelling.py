import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BUILDINGS = ROOT / "Content" / "Sprites" / "dragon-citadel" / "town" / "buildings"
TOWN_DATA = ROOT / "Content" / "Data" / "dragon-citadel" / "town-screen"
BACKGROUND = TOWN_DATA / "background.bmp"
CYAN = (0, 255, 255)

LEVEL8 = ("dwellingLvl8", "dwellingUpLvl8")
FULL_TOWN = (
    "mageGuild",
    "tavern",
    "castle",
    "capitol",
    "marketplace",
    "resourceSilo",
    "blacksmith",
    "special1",
    "special2",
    "special3",
    "special4",
    "grail",
    "dwellingUpLvl1",
    "dwellingUpLvl2",
    "dwellingUpLvl3",
    "dwellingUp3Lvl4",
    "dwellingUpLvl5",
    "dwellingUpLvl6",
    "dwellingUpLvl7",
    "dwellingUpLvl8",
    "special5",
)


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.convert("RGBA").getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Building image has no visible pixels")
    return bbox


def move_rgba(image: Image.Image, target: tuple[int, int]) -> Image.Image:
    source = image.convert("RGBA")
    bbox = alpha_bbox(source)
    crop = source.crop(bbox)
    output = Image.new("RGBA", source.size, (0, 0, 0, 0))
    output.alpha_composite(crop, target)
    return output


def move_mask(image: Image.Image, source_bbox: tuple[int, int, int, int], target: tuple[int, int]) -> Image.Image:
    source = image.convert("RGB")
    delta = (target[0] - source_bbox[0], target[1] - source_bbox[1])
    output = Image.new("RGB", source.size, CYAN)
    pixels = source.load()
    result = output.load()
    for y in range(source.height):
        for x in range(source.width):
            if pixels[x, y] == CYAN:
                continue
            tx = x + delta[0]
            ty = y + delta[1]
            if 0 <= tx < source.width and 0 <= ty < source.height:
                result[tx, ty] = pixels[x, y]
    return output


def compose_town(level8_target: tuple[int, int] | None = None) -> Image.Image:
    with Image.open(BACKGROUND) as image:
        town = image.convert("RGBA")

    for building in FULL_TOWN:
        path = BUILDINGS / building / "frame-00.png"
        with Image.open(path) as image:
            layer = image.convert("RGBA")
        if building == "dwellingUpLvl8" and level8_target is not None:
            layer = move_rgba(layer, level8_target)
        town.alpha_composite(layer)
    return town.convert("RGB")


def preview_options() -> None:
    options = (
        ("A - lower left", (335, 235)),
        ("B - under the stairs", (400, 235)),
        ("C - lower right", (465, 235)),
    )
    sheet = Image.new("RGB", (800, 1245), (18, 20, 25))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    y = 0
    for label, target in options:
        draw.text((12, y + 8), label, fill=(238, 224, 185), font=font)
        sheet.paste(compose_town(target), (0, y + 28))
        y += 415
    path = ROOT / "tools" / "town-level8-placement-options.png"
    sheet.save(path, optimize=True)


def apply_move(target: tuple[int, int]) -> None:
    for building in LEVEL8:
        frame_path = BUILDINGS / building / "frame-00.png"
        with Image.open(frame_path) as source:
            frame = source.convert("RGBA")
        bbox = alpha_bbox(frame)
        move_rgba(frame, target).save(frame_path, optimize=True)

        for mask_kind in ("areas", "borders"):
            mask_path = TOWN_DATA / mask_kind / f"{building}.bmp"
            with Image.open(mask_path) as source:
                moved = move_mask(source, bbox, target)
            moved.save(mask_path)

    final_town = compose_town()
    final_town.save(ROOT / "screenshots" / "town-screen.png", optimize=True)

    comparison_path = ROOT / "screenshots" / "town-screen-decluttered-before-after-1.5.4.png"
    if comparison_path.exists():
        with Image.open(comparison_path) as source:
            comparison = source.convert("RGB")
        comparison.paste(final_town, (800, 43))
        comparison.save(comparison_path, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--x", type=int, default=400)
    parser.add_argument("--y", type=int, default=235)
    args = parser.parse_args()

    if args.apply:
        apply_move((args.x, args.y))
    else:
        preview_options()


if __name__ == "__main__":
    main()
