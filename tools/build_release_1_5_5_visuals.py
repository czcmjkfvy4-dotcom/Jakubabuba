import argparse
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "Content"
DATA = CONTENT / "Data" / "dragon-citadel"
SPRITES = CONTENT / "Sprites" / "dragon-citadel"
CONFIG = CONTENT / "config" / "dragon-citadel"
SOURCE = ROOT / "tools" / "source-assets"
BUILDINGS = SPRITES / "town" / "buildings"
TOWN_DATA = DATA / "town-screen"
CYAN = (0, 255, 255)

TEMPLATE = (
    Path.home()
    / "Documents"
    / "My Games"
    / "vcmi"
    / "Mods"
    / "abyss-town"
    / "content"
    / "Data"
    / "abyss"
    / "siege"
)

FULL_TOWN = (
    "mageGuild5",
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
    "special5",
)

BATTLE_OUTLINE_COLORS = {
    "dcAzureDragon": (240, 248, 255),
    "dcBlackDragon": (245, 125, 44),
    "dcCrystalDragon": (255, 255, 0),
    "dcDiamondGolem": (255, 255, 0),
    "dcEnchanter": (47, 51, 55),
    "dcEternalStormDragon": (232, 236, 239),
    "dcFairieDragon": (255, 255, 0),
    "dcFirebird": (255, 255, 0),
    "dcGiant": (255, 255, 0),
    "dcGoldDragon": (255, 255, 0),
    "dcGoldGolem": (255, 255, 0),
    "dcPhoenix": (145, 235, 255),
    "dcRubyGolem": (240, 74, 98),
    "dcRustDragon": (255, 255, 0),
    "dcSharpshooter": (255, 255, 0),
    "dcStormDragon": (184, 196, 204),
    "dcTitan": (255, 226, 125),
}


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.convert("RGBA").getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Image has no visible pixels")
    return bbox


def keyed_rgba(path: Path) -> Image.Image:
    with Image.open(path) as source:
        image = source.convert("RGBA")
    key = image.getpixel((0, 0))[:3]
    pixels = []
    has_alpha = image.getchannel("A").getextrema() != (255, 255)
    for red, green, blue, source_alpha in image.getdata():
        is_cyan_key = red <= 8 and green >= 247 and blue >= 247
        is_corner_key = not has_alpha and (red, green, blue) == key
        alpha = 0 if is_cyan_key or is_corner_key else source_alpha
        pixels.append((red, green, blue, alpha))
    image.putdata(pixels)
    return image


def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    crop = image.convert("RGBA").crop(alpha_bbox(image))
    crop.thumbnail(size, Image.Resampling.LANCZOS)
    return crop


def transform_canvas(path: Path, scale: float, down: int) -> tuple[int, int, int, int]:
    with Image.open(path) as source:
        original = source.convert("RGBA")
    bbox = alpha_bbox(original)
    crop = original.crop(bbox)
    resized = crop.resize(
        (max(1, round(crop.width * scale)), max(1, round(crop.height * scale))),
        Image.Resampling.LANCZOS,
    )
    center_x = (bbox[0] + bbox[2]) // 2
    target_x = center_x - resized.width // 2
    target_y = bbox[3] + down - resized.height
    target_x = max(0, min(original.width - resized.width, target_x))
    target_y = max(0, min(original.height - resized.height, target_y))
    result = Image.new("RGBA", original.size, (0, 0, 0, 0))
    result.alpha_composite(resized, (target_x, target_y))
    result.save(path, optimize=True)
    return bbox


def transform_mask(path: Path, source_bbox: tuple[int, int, int, int], scale: float, down: int) -> None:
    with Image.open(path) as source:
        original = source.convert("RGB")
    crop = original.crop(source_bbox)
    resized = crop.resize(
        (max(1, round(crop.width * scale)), max(1, round(crop.height * scale))),
        Image.Resampling.NEAREST,
    )
    center_x = (source_bbox[0] + source_bbox[2]) // 2
    target_x = center_x - resized.width // 2
    target_y = source_bbox[3] + down - resized.height
    target_x = max(0, min(original.width - resized.width, target_x))
    target_y = max(0, min(original.height - resized.height, target_y))
    result = Image.new("RGB", original.size, CYAN)
    result.paste(resized, (target_x, target_y))
    result.save(path)


def enlarge_and_ground_town() -> None:
    for directory in sorted(BUILDINGS.iterdir()):
        if not directory.is_dir() or directory.name == "grail":
            continue
        name = directory.name
        if name in {"dwellingLvl8", "dwellingUpLvl8"}:
            scale = 1.0
            down = 0
        elif name in {"fort", "citadel", "castle"}:
            scale = 1.08
            down = 3
        elif name.startswith("dwelling"):
            scale = 1.16
            down = 4
        else:
            scale = 1.20
            down = 4
        frame = directory / "frame-00.png"
        if not frame.exists():
            continue
        bbox = transform_canvas(frame, scale, down)
        for mask_kind in ("areas", "borders"):
            mask = TOWN_DATA / mask_kind / f"{name}.bmp"
            if mask.exists():
                transform_mask(mask, bbox, scale, down)


def add_town_grounding_shadows() -> None:
    for directory in sorted(BUILDINGS.iterdir()):
        if not directory.is_dir() or directory.name == "grail":
            continue
        for frame_path in sorted(directory.glob("frame-*.png")):
            image = keyed_rgba(frame_path)
            bbox = alpha_bbox(image)
            width = max(18, bbox[2] - bbox[0])
            height = max(5, min(15, round((bbox[3] - bbox[1]) * 0.10)))
            shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(shadow, "RGBA")
            center_x = (bbox[0] + bbox[2]) // 2
            y = min(image.height - 3, bbox[3] - 4)
            draw.ellipse(
                (
                    center_x - round(width * 0.58),
                    y - height,
                    center_x + round(width * 0.58),
                    y + height,
                ),
                fill=(0, 0, 0, 95),
            )
            shadow = shadow.filter(ImageFilter.GaussianBlur(max(2, height // 3)))
            shadow.alpha_composite(image)
            shadow.save(frame_path, optimize=True)


def build_grail() -> None:
    source = keyed_rgba(SOURCE / "grail-storm.png")
    cloud = fit(source, (450, 245))
    output_dir = BUILDINGS / "grail"
    output_dir.mkdir(parents=True, exist_ok=True)
    union = Image.new("L", (800, 374), 0)
    images = []

    for frame_index in range(8):
        pulse_red = (0.28, 0.52, 1.0, 0.62, 0.35, 0.78, 1.0, 0.48)[frame_index]
        pulse_violet = (0.62, 1.0, 0.42, 0.78, 1.0, 0.35, 0.58, 0.9)[frame_index]
        animated = cloud.copy()
        pixels = []
        for red, green, blue, alpha in animated.getdata():
            if red > green * 1.25 and red > blue * 1.05 and red > 75:
                alpha = round(alpha * pulse_red)
            elif blue > red * 1.08 and blue > green * 1.05 and blue > 85:
                alpha = round(alpha * pulse_violet)
            pixels.append((red, green, blue, alpha))
        animated.putdata(pixels)
        canvas = Image.new("RGBA", (800, 374), (0, 0, 0, 0))
        x = 175 + (1 if frame_index in {2, 6} else 0)
        y = 0
        canvas.alpha_composite(animated, (x, y))
        canvas.save(output_dir / f"frame-{frame_index:02d}.png", optimize=True)
        union = ImageChops.lighter(union, canvas.getchannel("A"))
        images.append({"group": 0, "frame": frame_index, "file": f"frame-{frame_index:02d}"})

    (BUILDINGS / "grail.json").write_text(
        json.dumps(
            {"basepath": "dragon-citadel/town/buildings/grail/", "images": images},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    mask = union.point(lambda value: 255 if value > 24 else 0)
    for kind, color in (("areas", (255, 0, 0)), ("borders", (210, 180, 110))):
        result = Image.new("RGB", (800, 374), CYAN)
        fill = Image.new("RGB", result.size, color)
        result.paste(fill, mask=mask)
        result.save(TOWN_DATA / kind / "grail.bmp")


def paint_dragon_turret(canvas: Image.Image, cx: int, ground: int, scale: float, fire_step: int = 0, with_base: bool = True) -> None:
    draw = ImageDraw.Draw(canvas, "RGBA")

    def p(x: float, y: float) -> tuple[int, int]:
        return (round(cx + x * scale), round(ground + y * scale))

    dark = (11, 16, 24, 245)
    mid = (42, 50, 65, 245)
    light = (105, 116, 136, 210)
    gold = (126, 100, 42, 210)

    if with_base:
        draw.rectangle((p(-42, -38), p(42, 2)), fill=mid, outline=dark, width=max(1, round(2 * scale)))
        for x in (-34, -14, 6, 26):
            draw.rectangle((p(x, -52), p(x + 11, -34)), fill=(50, 59, 76, 245), outline=dark)
    draw.polygon((p(-20, -96), p(14, -110), p(28, -46), p(-28, -42)), fill=(35, 43, 58, 245), outline=dark)
    draw.polygon((p(-54, -108), p(-16, -134), p(42, -120), p(62, -96), p(24, -82), p(-34, -84)), fill=mid, outline=dark)
    draw.polygon((p(-28, -126), p(-18, -166), p(-4, -130)), fill=(94, 105, 124, 230), outline=dark)
    draw.polygon((p(18, -126), p(32, -160), p(34, -122)), fill=(88, 99, 118, 230), outline=dark)
    draw.polygon((p(-58, -104), p(-82, -118), p(-62, -90)), fill=(28, 35, 48, 235), outline=dark)
    draw.line((p(-32, -102), p(18, -110), p(48, -98)), fill=light, width=max(1, round(2 * scale)))
    draw.ellipse((p(20, -112), p(30, -102)), fill=(98, 210, 225, 230), outline=dark)
    if with_base:
        draw.line((p(-42, -26), p(38, -32)), fill=(104, 115, 136, 155), width=max(1, round(2 * scale)))
    draw.line((p(-2, -90), p(8, -54)), fill=gold, width=max(1, round(2 * scale)))

    if fire_step:
        length = 32 + fire_step * 13
        spread = 6 + fire_step * 3
        mouth = p(58, -98)
        tip = p(58 + length, -99 + (fire_step % 2) * 3)
        draw.polygon((p(54, -103 - spread), tip, p(54, -93 + spread)), fill=(2, 1, 3, 205))
        draw.polygon((p(58, -101 - spread * 0.55), p(58 + length * 0.74, -99), p(58, -95 + spread * 0.55)), fill=(80, 0, 16, 210))
        draw.line((mouth, tip), fill=(182, 24, 36, 230), width=max(1, round(3 * scale)))


def stone_turret_head(max_size: tuple[int, int]) -> Image.Image:
    source = keyed_rgba(SPRITES / "creatures" / "dcUltimateDragon" / "battle" / "g00-f000.png")
    head = source.crop((230, 95, 380, 235))
    head = head.crop(alpha_bbox(head))
    return ImageEnhance.Contrast(style_siege_piece(fit(head, max_size))).enhance(1.08)


def build_turret_animation() -> None:
    base = Image.new("RGBA", (450, 400), (0, 0, 0, 0))
    head = stone_turret_head((78, 74))
    x = 225 - head.width // 2
    y = 300 - head.height
    base.alpha_composite(head, (x, y))
    battle_dir = SPRITES / "creatures" / "dcDragonTurret" / "battle"
    map_dir = SPRITES / "creatures" / "dcDragonTurret" / "map"
    battle_dir.mkdir(parents=True, exist_ok=True)
    map_dir.mkdir(parents=True, exist_ok=True)

    attack_frames = []
    for frame_index, fire_step in enumerate((1, 2, 3, 2)):
        frame = base.copy()
        draw = ImageDraw.Draw(frame, "RGBA")
        mouth = (x + round(head.width * 0.86), y + round(head.height * 0.62))
        length = 34 + fire_step * 16
        spread = 6 + fire_step * 4
        draw.polygon(
            ((mouth[0] - 2, mouth[1] - spread), (mouth[0] + length, mouth[1] - 3), (mouth[0], mouth[1] + spread)),
            fill=(3, 1, 5, 210),
        )
        draw.polygon(
            ((mouth[0] + 3, mouth[1] - spread // 2), (mouth[0] + round(length * 0.78), mouth[1]), (mouth[0] + 3, mouth[1] + spread // 2)),
            fill=(92, 0, 20, 220),
        )
        draw.line((mouth[0], mouth[1], mouth[0] + length, mouth[1] - 2), fill=(192, 24, 38, 235), width=3)
        attack_frames.append(frame)

    images = []
    for group in (0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 14, 15, 16, 20):
        count = 4 if group == 0 else 1
        for frame_index in range(count):
            filename = f"g{group:02d}-f{frame_index:03d}"
            frame = base.copy()
            if group == 0 and frame_index % 2:
                frame = ImageEnhance.Brightness(frame).enhance(1.04)
            frame.save(battle_dir / f"{filename}.png", optimize=True)
            images.append({"group": group, "frame": frame_index, "file": filename})
    for group in (11, 12, 13):
        for frame_index, frame in enumerate(attack_frames):
            filename = f"g{group:02d}-f{frame_index:03d}"
            frame.save(battle_dir / f"{filename}.png", optimize=True)
            images.append({"group": group, "frame": frame_index, "file": filename})

    (SPRITES / "creatures" / "dcDragonTurret" / "battle.json").write_text(
        json.dumps(
            {"basepath": "dragon-citadel/creatures/dcDragonTurret/battle/", "images": images},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    map_frame = Image.new("RGBA", (173, 173), (0, 0, 0, 0))
    map_head = stone_turret_head((120, 118))
    map_frame.alpha_composite(map_head, ((173 - map_head.width) // 2, 166 - map_head.height))
    map_frame.save(map_dir / "frame-00.png", optimize=True)
    (SPRITES / "creatures" / "dcDragonTurret" / "map.json").write_text(
        json.dumps(
            {
                "basepath": "dragon-citadel/creatures/dcDragonTurret/map/",
                "images": [{"group": 0, "frame": 0, "file": "frame-00"}],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def clean_alpha(subject: Image.Image) -> Image.Image:
    alpha = subject.getchannel("A")
    alpha = alpha.point(lambda value: 0 if value < 92 else min(255, round((value - 92) * 1.57)))
    subject.putalpha(alpha)
    return subject


def rebuild_creature_icons() -> None:
    creatures = json.loads((CONFIG / "creatures.json").read_text(encoding="utf-8-sig"))
    icon_dir = DATA / "creatures" / "icons"
    background_path = DATA / "interface" / "creature-background-130.png"
    with Image.open(background_path) as source:
        background_source = source.convert("RGB")

    for unit, config in creatures.items():
        graphics = config.get("graphics", {})
        animation = graphics.get("animation")
        if not animation:
            continue
        frame_path = SPRITES / Path(animation).relative_to("dragon-citadel") / "g00-f000.png"
        if not frame_path.exists():
            continue
        with Image.open(frame_path) as source:
            subject_source = source.convert("RGBA")
        for suffix, size in (("large", (58, 64)), ("small", (32, 32))):
            background = background_source.resize(size, Image.Resampling.LANCZOS).convert("RGBA")
            margin = 3 if suffix == "large" else 2
            subject = fit(subject_source, (size[0] - margin * 2, round(size[1] * 0.76)))
            subject = clean_alpha(subject)
            x = (size[0] - subject.width) // 2
            y = max(1, min(round(size[1] * 0.52 - subject.height / 2), size[1] - subject.height - 2))
            background.alpha_composite(subject, (x, y))
            background.convert("RGB").save(icon_dir / f"{unit}-{suffix}.png", optimize=True)


def build_endgame_building_icons() -> None:
    icon_dir = SPRITES / "town" / "building-icons"
    animation_path = SPRITES / "town" / "building-icons.json"
    animation = json.loads(animation_path.read_text(encoding="utf-8-sig"))
    images = [entry for entry in animation["images"] if entry.get("frame") not in {150, 151}]

    for frame, creature in ((150, "dcUltimateDragon"), (151, "dcAbsoluteDragon")):
        canvas = Image.new("RGBA", (150, 70), (7, 9, 12, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw.rectangle((0, 0, 149, 69), outline=(176, 139, 57, 255), width=1)
        draw.rectangle((2, 2, 147, 67), outline=(72, 58, 31, 255), width=1)
        draw.line((4, 61, 145, 61), fill=(184, 130, 38, 255), width=2)

        frame_path = SPRITES / "creatures" / creature / "battle" / "g00-f000.png"
        with Image.open(frame_path) as source:
            subject = fit(source.convert("RGBA"), (70, 58))
        canvas.alpha_composite(subject, ((150 - subject.width) // 2, 59 - subject.height))
        canvas.convert("RGB").save(icon_dir / f"frame-{frame:03}.png", optimize=True)
        images.append({"group": 0, "frame": frame, "file": f"frame-{frame:03}"})

    animation["images"] = sorted(images, key=lambda entry: (entry.get("group", 0), entry["frame"]))
    animation_path.write_text(json.dumps(animation, indent=2) + "\n", encoding="utf-8")


def style_siege_piece(image: Image.Image) -> Image.Image:
    styled = image.convert("RGBA")
    pixels = []
    for red, green, blue, alpha in styled.getdata():
        if alpha == 0:
            pixels.append((0, 0, 0, 0))
            continue
        lum = round(red * 0.30 + green * 0.59 + blue * 0.11)
        color = (10 + round(lum * 0.39), 14 + round(lum * 0.41), 21 + round(lum * 0.45), alpha)
        pixels.append(color)
    styled.putdata(pixels)
    return ImageEnhance.Contrast(styled).enhance(1.15)


def style_siege_background(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image.convert("RGB"))
    stone = ImageOps.colorize(gray, black=(4, 6, 9), white=(105, 111, 122))
    stone = ImageEnhance.Contrast(stone).enhance(1.22)
    return ImageEnhance.Brightness(stone).enhance(0.78)


def make_tower_piece(turret: Image.Image, template: Image.Image, state: str, head_only: bool) -> Image.Image:
    size = template.size
    canvas = style_siege_piece(template)
    head = stone_turret_head((max(1, round(size[0] * 0.50)), max(1, round(size[1] * (0.32 if head_only else 0.42)))))
    canvas.alpha_composite(head, ((size[0] - head.width) // 2, max(0, round(size[1] * 0.08))))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.line((3, size[1] - 7, size[0] - 4, size[1] - 12), fill=(100, 110, 128, 170), width=2)
    draw.rectangle((0, size[1] - 4, size[0], size[1]), fill=(7, 10, 15, 160))
    if state == "2":
        draw.polygon(((size[0] * 0.62, 0), (size[0], 0), (size[0], size[1] * 0.38)), fill=(0, 0, 0, 0))
        draw.line((round(size[0] * 0.35), round(size[1] * 0.18), round(size[0] * 0.52), round(size[1] * 0.62)), fill=(8, 10, 15, 170), width=2)
        canvas = ImageEnhance.Brightness(canvas).enhance(0.82)
    elif state == "C":
        draw.rectangle((0, 0, size[0], round(size[1] * 0.48)), fill=(0, 0, 0, 0))
        canvas = ImageEnhance.Brightness(canvas).enhance(0.55)
    return canvas


def build_siege() -> None:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Siege template not found: {TEMPLATE}")
    output = DATA / "siege"
    output.mkdir(parents=True, exist_ok=True)
    turret = keyed_rgba(SOURCE / "dragon-turret.png")

    background_path = next(TEMPLATE.glob("*BACK.png"))
    with Image.open(background_path) as source:
        background = style_siege_background(source)
    background.save(output / "SGDCBACK.png", optimize=True)

    for source_path in TEMPLATE.iterdir():
        if not source_path.is_file() or not source_path.stem.lower().startswith("sgdn"):
            continue
        suffix = source_path.stem[4:].upper()
        if suffix == "BACK":
            continue
        image = keyed_rgba(source_path)
        if suffix.startswith("TW2"):
            state = suffix[-1]
            image = make_tower_piece(turret, image, state, False)
        elif suffix.startswith("TW1"):
            state = suffix[-1]
            image = make_tower_piece(turret, image, state, True)
        else:
            image = style_siege_piece(image)
        image.save(output / f"SGDC{suffix}.png", optimize=True)

    for suffix in ("TPW1", "TPWL"):
        source = output / f"SGDC{suffix}.png"
        if not source.exists():
            fallback = output / ("SGDCTPW1.png" if suffix == "TPWL" else "SGDCTPWL.png")
            if fallback.exists():
                shutil.copy2(fallback, source)

    icon_dir = SPRITES / "icons"
    for name, size in (("towerLarge.png", (58, 64)), ("towerSmall.png", (32, 32))):
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
        head = stone_turret_head((max(1, size[0] - 4), max(1, size[1] - 4)))
        canvas.alpha_composite(head, ((size[0] - head.width) // 2, size[1] - head.height - 1))
        canvas.save(icon_dir / name, optimize=True)


def remove_battle_outlines() -> None:
    changed_frames = 0
    removed_pixels = 0
    for creature, outline_color in BATTLE_OUTLINE_COLORS.items():
        battle_dir = SPRITES / "creatures" / creature / "battle"
        for frame_path in sorted(battle_dir.glob("g??-f???.png")):
            with Image.open(frame_path) as source:
                image = source.convert("RGBA")
            pixels = image.load()
            width, height = image.size
            boundary = []
            for y in range(height):
                for x in range(width):
                    if pixels[x, y][3] == 0:
                        continue
                    if any(
                        pixels[nx, ny][3] == 0
                        for ny in range(max(0, y - 1), min(height, y + 2))
                        for nx in range(max(0, x - 1), min(width, x + 2))
                    ):
                        boundary.append((x, y))

            def matches_outline(color: tuple[int, int, int]) -> bool:
                return max(abs(color[channel] - outline_color[channel]) for channel in range(3)) <= 8

            outline_count = sum(1 for x, y in boundary if matches_outline(pixels[x, y][:3]))
            if outline_count < 8:
                continue

            to_remove = []
            for x, y in boundary:
                red, green, blue, alpha = pixels[x, y]
                is_chroma_remnant = (
                    green > 245 and red < 12 and blue < 12
                ) or (
                    red > 170 and blue > 245 and green < 12
                )
                if matches_outline((red, green, blue)) or alpha <= 200 or is_chroma_remnant:
                    to_remove.append((x, y))

            for x, y in to_remove:
                pixels[x, y] = (0, 0, 0, 0)
            image.save(frame_path, optimize=True)
            changed_frames += 1
            removed_pixels += len(to_remove)
    print(f"Battle outline cleanup: {changed_frames} frames, {removed_pixels} pixels removed")


def strengthen_map_stages() -> None:
    stage_heights = {
        "town-village": 132,
        "town-fort": 146,
        "town-citadel": 154,
        "town-castle": 165,
        "town-capitol": 169,
    }
    for stage, height in stage_heights.items():
        path = SPRITES / "map" / stage / "frame-00.png"
        image = keyed_rgba(path)
        subject = fit(image, (169, height))
        canvas = Image.new("RGBA", (173, 173), (0, 0, 0, 0))
        canvas.alpha_composite(subject, ((173 - subject.width) // 2, 170 - subject.height))
        if stage == "town-capitol":
            draw = ImageDraw.Draw(canvas, "RGBA")
            draw.line((47, 30, 62, 54, 54, 70), fill=(215, 245, 255, 210), width=2)
            draw.line((121, 24, 109, 46, 118, 62), fill=(145, 70, 255, 220), width=2)
        canvas.save(path, optimize=True)


def compose_town_preview() -> None:
    faction = json.loads((CONFIG / "faction.json").read_text(encoding="utf-8-sig"))
    structures = faction["dragonCitadel"]["town"]["structures"]
    with Image.open(TOWN_DATA / "background.bmp") as source:
        town = source.convert("RGBA")
    layers = sorted(FULL_TOWN, key=lambda name: structures.get(name, {}).get("z", 0))
    for building in layers:
        animation = structures[building]["animation"].split("/")[-1]
        frame_dir = BUILDINGS / animation
        frames = sorted(frame_dir.glob("frame-*.png"))
        if not frames:
            continue
        with Image.open(frames[0]) as source:
            town.alpha_composite(source.convert("RGBA"))
    town.convert("RGB").save(ROOT / "screenshots" / "town-screen.png", optimize=True)


def compose_siege_preview() -> None:
    siege = DATA / "siege"
    with Image.open(siege / "SGDCBACK.png") as source:
        canvas = source.convert("RGBA")
    layers = (
        ("TPW1", 608, 50),
        ("WA5", 494, 53),
        ("WA61", 523, 56),
        ("WA41", 477, 180),
        ("ARCH", 471, 164),
        ("DRW1", 395, 260),
        ("WA31", 471, 296),
        ("WA2", 522, 305),
        ("WA11", 559, 448),
        ("MAN1", 732, 162),
        ("TW21", 565, 15),
        ("TW11", 580, 495),
    )
    for suffix, x, y in layers:
        path = siege / f"SGDC{suffix}.png"
        if path.exists():
            with Image.open(path) as source:
                canvas.alpha_composite(source.convert("RGBA"), (x, y))
    turret_frame = SPRITES / "creatures" / "dcDragonTurret" / "battle" / "g00-f000.png"
    with Image.open(turret_frame) as source:
        shooter = source.convert("RGBA")
    for x, y in ((361, 293), (530, -33), (347, -187)):
        canvas.alpha_composite(shooter, (x, y))
    canvas.convert("RGB").save(ROOT / "screenshots" / "dragon-citadel-siege-1.5.5.png", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview-only", action="store_true")
    parser.add_argument("--rebuild-corrections", action="store_true")
    parser.add_argument("--remove-battle-outlines", action="store_true")
    parser.add_argument("--rebuild-siege", action="store_true")
    parser.add_argument("--ground-town-buildings", action="store_true")
    parser.add_argument("--repair-building-icons", action="store_true")
    args = parser.parse_args()
    if args.remove_battle_outlines:
        remove_battle_outlines()
    elif args.repair_building_icons:
        build_endgame_building_icons()
    elif args.rebuild_siege:
        build_turret_animation()
        build_siege()
    elif args.ground_town_buildings:
        add_town_grounding_shadows()
    elif args.rebuild_corrections:
        build_grail()
        build_siege()
        strengthen_map_stages()
    elif not args.preview_only:
        enlarge_and_ground_town()
        build_grail()
        build_turret_animation()
        rebuild_creature_icons()
        build_endgame_building_icons()
        build_siege()
        strengthen_map_stages()
    compose_town_preview()
    compose_siege_preview()


if __name__ == "__main__":
    main()
