from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


PROJECT = Path(r"C:\Users\GRACOMM\Desktop\smocze miasto heroes 3\dragon-citadel")
ORIGINALS = PROJECT / "tools" / "town-icon-generation" / "original-icons"
ICON_DIR = PROJECT / "Content" / "Data" / "dragon-citadel" / "town-icons"
PREVIEW = PROJECT / "screenshots" / "town-selection-icons-before-after-1.5.4.png"


def enhance(original: Image.Image) -> Image.Image:
    alpha = original.convert("RGBA").getchannel("A")
    image = ImageEnhance.Color(original.convert("RGB")).enhance(1.65)
    image = ImageEnhance.Contrast(image).enhance(1.18)
    image = ImageEnhance.Brightness(image).enhance(1.08)
    image = image.filter(ImageFilter.UnsharpMask(radius=0.65, percent=120, threshold=2))
    image = image.convert("RGBA")
    image.putalpha(alpha)
    return image


def make_preview(originals: dict[str, Image.Image], updated: dict[str, Image.Image]) -> None:
    order = [
        "village-normal-large",
        "village-built-large",
        "fort-normal-large",
        "fort-built-large",
        "village-normal-small",
        "village-built-small",
        "fort-normal-small",
        "fort-built-small",
    ]
    scale = 5
    tile_width = 610
    tile_height = 360
    canvas = Image.new("RGB", (tile_width * 2, tile_height * 4), (24, 27, 33))
    draw = ImageDraw.Draw(canvas)

    for index, key in enumerate(order):
        col = index % 2
        row = index // 2
        x = col * tile_width
        y = row * tile_height
        old = originals[key].convert("RGB").resize(
            (originals[key].width * scale, originals[key].height * scale),
            Image.Resampling.NEAREST,
        )
        new = updated[key].convert("RGB").resize(
            (updated[key].width * scale, updated[key].height * scale),
            Image.Resampling.NEAREST,
        )
        canvas.paste(old, (x + 5, y + 25))
        canvas.paste(new, (x + 315, y + 25))
        draw.text((x + 5, y + 5), f"{key}: original", fill=(240, 240, 242))
        draw.text((x + 315, y + 5), "color corrected", fill=(240, 240, 242))

    canvas.save(PREVIEW, optimize=True)


def main() -> None:
    originals = {
        path.stem: Image.open(path).convert("RGBA")
        for path in ORIGINALS.glob("*.png")
    }
    if len(originals) != 8:
        raise RuntimeError(f"Expected 8 original town icons, found {len(originals)}")

    updated = {key: enhance(image) for key, image in originals.items()}
    for key, image in updated.items():
        image.save(ICON_DIR / f"{key}.png", optimize=True)
    make_preview(originals, updated)


if __name__ == "__main__":
    main()
