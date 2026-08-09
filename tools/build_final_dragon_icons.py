from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Content" / "Data" / "dragon-citadel"
SPRITES = ROOT / "Content" / "Sprites" / "dragon-citadel"
OUTPUT = ROOT / "tools" / "final-dragon-icon-generation" / "candidates"

UNITS = (
    ("dcUltimateDragon", "Ultimate Dragon"),
    ("dcAbsoluteDragon", "Absolute Dragon"),
)


def fit_subject(frame: Image.Image, size: tuple[int, int]) -> Image.Image:
    frame = frame.convert("RGBA")
    bbox = frame.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Dragon frame has no visible pixels")

    subject = frame.crop(bbox)
    subject.thumbnail(size, Image.Resampling.LANCZOS)
    return subject


def build_icon(unit: str, output_size: tuple[int, int]) -> Image.Image:
    background_path = DATA / "interface" / "creature-background-130.png"
    frame_path = SPRITES / "creatures" / unit / "battle" / "g00-f000.png"

    with Image.open(background_path) as background_source:
        background = background_source.convert("RGB").resize(
            output_size, Image.Resampling.LANCZOS
        ).convert("RGBA")

    margin_x = 2 if output_size[0] <= 32 else 3
    max_width = output_size[0] - margin_x * 2
    max_height = int(output_size[1] * 0.72)

    with Image.open(frame_path) as frame:
        subject = fit_subject(frame, (max_width, max_height))

    x = (output_size[0] - subject.width) // 2
    y = int(output_size[1] * 0.52 - subject.height / 2)
    y = max(2, min(y, output_size[1] - subject.height - 3))

    alpha = subject.getchannel("A")
    shadow_alpha = alpha.filter(ImageFilter.GaussianBlur(max(0.6, output_size[0] / 58)))
    shadow = Image.new("RGBA", subject.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_alpha.point(lambda value: int(value * 0.65)))
    background.alpha_composite(shadow, (x + 1, y + 2))
    background.alpha_composite(subject, (x, y))
    return background.convert("RGB")


def build_preview(new_icons: dict[str, Image.Image]) -> None:
    preview = Image.new("RGB", (960, 610), (18, 20, 25))
    draw = ImageDraw.Draw(preview)
    font = ImageFont.load_default()
    draw.text((24, 18), "Level 8 recruitment portraits - before / fitted", fill=(238, 224, 185), font=font)

    icon_dir = DATA / "creatures" / "icons"
    for row, (unit, label) in enumerate(UNITS):
        y = 65 + row * 170
        with Image.open(icon_dir / f"{unit}-large.png") as old_source:
            old = old_source.convert("RGB")
        new = new_icons[unit]

        draw.text((24, y), label, fill=(230, 230, 230), font=font)
        draw.text((235, y), "Before", fill=(180, 185, 195), font=font)
        draw.text((555, y), "Fitted", fill=(180, 185, 195), font=font)
        preview.paste(old.resize((232, 256), Image.Resampling.NEAREST), (180, y + 20))
        preview.paste(new.resize((232, 256), Image.Resampling.NEAREST), (500, y + 20))

    preview.save(OUTPUT / "final-dragon-icons-before-after.png")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    new_icons = {}
    for unit, _ in UNITS:
        large = build_icon(unit, (58, 64))
        small = build_icon(unit, (32, 32))
        large.save(OUTPUT / f"{unit}-large.png", optimize=True)
        small.save(OUTPUT / f"{unit}-small.png", optimize=True)
        new_icons[unit] = large

    build_preview(new_icons)


if __name__ == "__main__":
    main()
