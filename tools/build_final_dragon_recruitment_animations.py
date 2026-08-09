from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CREATURES = ROOT / "Content" / "Sprites" / "dragon-citadel" / "creatures"
UNITS = ("dcUltimateDragon", "dcAbsoluteDragon")

# VCMI 1.7.4 displays recruitment animations from this source rectangle.
PREVIEW_RECT = (150, 155, 100, 130)
MARGIN = 4


def union_bbox(paths: list[Path]) -> tuple[int, int, int, int]:
    boxes = []
    for path in paths:
        with Image.open(path) as image:
            bbox = image.convert("RGBA").getchannel("A").getbbox()
            if bbox:
                boxes.append(bbox)
    if not boxes:
        raise ValueError(f"Animation group has no visible frames: {paths[0].parent}")
    return (
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    )


def build_unit(unit: str) -> None:
    source = CREATURES / unit / "battle"
    destination = CREATURES / unit / "recruitment-preview"
    destination.mkdir(parents=True, exist_ok=True)

    groups: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(source.glob("g??-f???.png")):
        groups[path.name[:3]].append(path)

    rect_x, rect_y, rect_w, rect_h = PREVIEW_RECT
    max_w = rect_w - MARGIN * 2
    max_h = rect_h - MARGIN * 2

    for paths in groups.values():
        bbox = union_bbox(paths)
        crop_w = bbox[2] - bbox[0]
        crop_h = bbox[3] - bbox[1]
        scale = min(max_w / crop_w, max_h / crop_h)
        target_w = max(1, round(crop_w * scale))
        target_h = max(1, round(crop_h * scale))
        target_x = rect_x + (rect_w - target_w) // 2
        target_y = rect_y + rect_h - target_h - MARGIN

        for path in paths:
            with Image.open(path) as image:
                source_frame = image.convert("RGBA")
                group_crop = source_frame.crop(bbox)
                fitted = group_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
                output = Image.new("RGBA", source_frame.size, (0, 0, 0, 0))
                output.alpha_composite(fitted, (target_x, target_y))
                output.save(destination / path.name, optimize=True)


def build_preview_sheet() -> None:
    sheet = Image.new("RGB", (700, 430), (18, 20, 25))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((24, 20), "Level 8 animated recruitment preview", fill=(238, 224, 185), font=font)
    draw.text((24, 42), "The complete creature stays inside VCMI's 100 x 130 preview area.", fill=(185, 190, 200), font=font)

    background_path = ROOT / "Content" / "Data" / "dragon-citadel" / "interface" / "creature-background-130.png"
    with Image.open(background_path) as source:
        background = source.convert("RGBA")

    rect_x, rect_y, rect_w, rect_h = PREVIEW_RECT
    labels = ("Ultimate Dragon", "Absolute Dragon")
    for index, (unit, label) in enumerate(zip(UNITS, labels)):
        with Image.open(CREATURES / unit / "recruitment-preview" / "g00-f000.png") as frame:
            crop = frame.convert("RGBA").crop((rect_x, rect_y, rect_x + rect_w, rect_y + rect_h))
        panel = background.copy()
        panel.alpha_composite(crop)
        enlarged = panel.convert("RGB").resize((250, 325), Image.Resampling.NEAREST)
        x = 55 + index * 330
        sheet.paste(enlarged, (x, 78))
        draw.text((x, 62), label, fill=(230, 230, 230), font=font)

    output = ROOT / "screenshots" / "level8-recruitment-preview-1.5.4.png"
    sheet.save(output, optimize=True)


def main() -> None:
    for unit in UNITS:
        build_unit(unit)
    build_preview_sheet()


if __name__ == "__main__":
    main()
