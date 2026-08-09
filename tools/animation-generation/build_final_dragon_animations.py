from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


PROJECT = Path(r"C:\Users\GRACOMM\Desktop\smocze miasto heroes 3\dragon-citadel")
REFERENCE_MOD = Path(
    r"C:\Users\GRACOMM\Desktop\smocze miasto heroes 3\backups"
    r"\dragon-citadel-installed-20260801-215914"
)
TOOLS = PROJECT / "tools" / "animation-generation"
SCREENSHOTS = PROJECT / "screenshots"
SPRITES = PROJECT / "Content" / "Sprites" / "dragon-citadel" / "creatures"
REFERENCE_SPRITES = (
    REFERENCE_MOD / "Content" / "Sprites" / "dragon-citadel" / "creatures"
)

CANVAS_SIZE = (450, 400)
CELL_GRID = 4
GROUND_Y = 285

TARGET_GROUPS = {0, 3, 11, 12, 13, 17, 18, 19, 20, 21}


def cell_bounds(sheet: Image.Image, index: int) -> tuple[int, int, int, int]:
    col = index % CELL_GRID
    row = index // CELL_GRID
    width, height = sheet.size
    return (
        round(col * width / CELL_GRID),
        round(row * height / CELL_GRID),
        round((col + 1) * width / CELL_GRID),
        round((row + 1) * height / CELL_GRID),
    )


def box_distance(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    dx = max(a[0] - b[2], b[0] - a[2], 0)
    dy = max(a[1] - b[3], b[1] - a[3], 0)
    return math.hypot(dx, dy)


def extract_element(
    sheet: Image.Image, index: int, padding: int = 80
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    """Extract one sprite while recovering fire or wings crossing a grid boundary."""
    x0, y0, x1, y1 = cell_bounds(sheet, index)
    ex0 = max(0, x0 - padding)
    ey0 = max(0, y0 - padding)
    ex1 = min(sheet.width, x1 + padding)
    ey1 = min(sheet.height, y1 + padding)
    expanded = sheet.crop((ex0, ey0, ex1, ey1)).convert("RGBA")

    alpha = np.asarray(expanded.getchannel("A"))
    labels, count = ndimage.label(alpha > 8)
    if count == 0:
        raise ValueError(f"No visible sprite in cell {index}")

    central = labels[y0 - ey0 : y1 - ey0, x0 - ex0 : x1 - ex0]
    overlaps = np.bincount(central.ravel(), minlength=count + 1)
    overlaps[0] = 0
    main_label = int(overlaps.argmax())

    objects = ndimage.find_objects(labels)
    main_slice = objects[main_label - 1]
    main_box = (
        main_slice[1].start,
        main_slice[0].start,
        main_slice[1].stop,
        main_slice[0].stop,
    )

    keep = labels == main_label
    for label_id, component_slice in enumerate(objects, start=1):
        if label_id == main_label or component_slice is None:
            continue
        component_box = (
            component_slice[1].start,
            component_slice[0].start,
            component_slice[1].stop,
            component_slice[0].stop,
        )
        touches_expanded_edge = (
            component_box[0] == 0
            or component_box[1] == 0
            or component_box[2] == expanded.width
            or component_box[3] == expanded.height
        )
        area = int(np.count_nonzero(labels == label_id))
        if not touches_expanded_edge and area >= 2 and box_distance(main_box, component_box) <= 60:
            keep |= labels == label_id

    # Keep the antialiased edge around selected connected components.
    keep = ndimage.binary_dilation(keep, iterations=2)
    cleaned = np.asarray(expanded).copy()
    cleaned[~keep] = 0
    cleaned_image = Image.fromarray(cleaned, "RGBA")
    bbox = cleaned_image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"Sprite cleanup removed cell {index}")

    global_bbox = (bbox[0] + ex0, bbox[1] + ey0, bbox[2] + ex0, bbox[3] + ey0)
    return cleaned_image.crop(bbox), global_bbox


def paste_clipped(canvas: Image.Image, element: Image.Image, x: int, y: int) -> None:
    left = max(0, -x)
    top = max(0, -y)
    right = min(element.width, canvas.width - x)
    bottom = min(element.height, canvas.height - y)
    if right <= left or bottom <= top:
        return
    cropped = element.crop((left, top, right, bottom))
    canvas.alpha_composite(cropped, (max(0, x), max(0, y)))


def stage_movement(
    sheet: Image.Image,
    index: int,
    *,
    center_y: int | None = None,
    bottom_y: int | None = None,
) -> Image.Image:
    element, _ = extract_element(sheet, index)
    canvas = Image.new("RGBA", CANVAS_SIZE)
    x = round((CANVAS_SIZE[0] - element.width) / 2)
    if bottom_y is not None:
        y = bottom_y - element.height
    elif center_y is not None:
        y = round(center_y - element.height / 2)
    else:
        raise ValueError("Movement frame requires center_y or bottom_y")
    paste_clipped(canvas, element, x, y)
    return canvas


def stage_action_row(sheet: Image.Image, row: int) -> list[Image.Image]:
    reference_index = row * CELL_GRID
    _, reference_box = extract_element(sheet, reference_index)
    cell_x0, cell_y0, cell_x1, _ = cell_bounds(sheet, reference_index)
    row_offset_y = GROUND_Y - (reference_box[3] - cell_y0)

    frames: list[Image.Image] = []
    for col in range(CELL_GRID):
        index = reference_index + col
        element, global_box = extract_element(sheet, index)
        x0, y0, x1, _ = cell_bounds(sheet, index)
        cell_width = x1 - x0
        canvas = Image.new("RGBA", CANVAS_SIZE)
        x = round((CANVAS_SIZE[0] - cell_width) / 2 + (global_box[0] - x0))
        y = round(row_offset_y + (global_box[1] - y0))
        paste_clipped(canvas, element, x, y)
        frames.append(canvas)
    return frames


def save_group(frames: list[Image.Image], battle_dir: Path, group: int) -> None:
    for frame_index, frame in enumerate(frames):
        frame.save(battle_dir / f"g{group:02d}-f{frame_index:03d}.png", optimize=True)


def restore_reference_creature(creature: str) -> tuple[Path, dict]:
    source = REFERENCE_SPRITES / creature
    destination = SPRITES / creature
    battle_dir = destination / "battle"
    battle_dir.mkdir(parents=True, exist_ok=True)
    for png in (source / "battle").glob("*.png"):
        shutil.copy2(png, battle_dir / png.name)
    with (source / "battle.json").open("r", encoding="utf-8") as handle:
        battle_json = json.load(handle)
    return battle_dir, battle_json


def update_battle_json(
    creature: str,
    battle_json: dict,
    group_counts: dict[int, int],
    battle_dir: Path,
) -> None:
    images = [
        image for image in battle_json["images"] if int(image["group"]) not in TARGET_GROUPS
    ]
    for group, count in group_counts.items():
        for frame in range(count):
            images.append(
                {
                    "group": group,
                    "frame": frame,
                    "file": f"g{group:02d}-f{frame:03d}",
                }
            )
    battle_json["images"] = sorted(images, key=lambda item: (item["group"], item["frame"]))

    json_path = SPRITES / creature / "battle.json"
    with json_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(battle_json, handle, ensure_ascii=True, indent=2)
        handle.write("\n")

    referenced = {f"{item['file']}.png" for item in battle_json["images"]}
    resolved_battle = battle_dir.resolve()
    if SPRITES.resolve() not in resolved_battle.parents:
        raise RuntimeError(f"Unsafe battle directory: {resolved_battle}")
    for png in battle_dir.glob("*.png"):
        if png.name not in referenced:
            png.unlink()


def preview_background(frame: Image.Image) -> Image.Image:
    background = Image.new("RGBA", frame.size, (27, 29, 35, 255))
    background.alpha_composite(frame)
    return background.convert("RGB")


def save_contact_sheet(frames: list[Image.Image], labels: list[str], path: Path) -> None:
    columns = 4
    thumb_size = (225, 200)
    rows = math.ceil(len(frames) / columns)
    sheet = Image.new("RGB", (columns * thumb_size[0], rows * (thumb_size[1] + 22)), (27, 29, 35))
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames):
        thumb = preview_background(frame).resize(thumb_size, Image.Resampling.LANCZOS)
        x = (index % columns) * thumb_size[0]
        y = (index // columns) * (thumb_size[1] + 22)
        sheet.paste(thumb, (x, y))
        draw.text((x + 6, y + thumb_size[1] + 4), labels[index], fill=(235, 235, 238))
    sheet.save(path, quality=94)


def save_gif(frames: list[Image.Image], path: Path, durations: list[int]) -> None:
    rendered = [preview_background(frame) for frame in frames]
    rendered[0].save(
        path,
        save_all=True,
        append_images=rendered[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )


def build_creature(
    creature: str,
    flight_sheet_name: str,
    action_sheet_name: str,
    movement_specs: dict[int, list[tuple[int, str, int]]],
) -> None:
    battle_dir, battle_json = restore_reference_creature(creature)
    flight_sheet = Image.open(TOOLS / flight_sheet_name).convert("RGBA")
    action_sheet = Image.open(TOOLS / action_sheet_name).convert("RGBA")

    movement_frames: list[Image.Image] = []
    movement_labels: list[str] = []
    group_counts: dict[int, int] = {}
    for group, specs in movement_specs.items():
        frames = []
        for index, anchor, value in specs:
            kwargs = {"bottom_y": value} if anchor == "bottom" else {"center_y": value}
            frames.append(stage_movement(flight_sheet, index, **kwargs))
        save_group(frames, battle_dir, group)
        group_counts[group] = len(frames)
        movement_frames.extend(frames)
        movement_labels.extend([f"group {group}, frame {i}" for i in range(len(frames))])

    action_frames: list[Image.Image] = []
    action_labels: list[str] = []
    for row, regular_group, special_group in ((0, 11, 17), (1, 12, 18), (2, 13, 19)):
        frames = stage_action_row(action_sheet, row)
        save_group(frames, battle_dir, regular_group)
        save_group(frames, battle_dir, special_group)
        group_counts[regular_group] = len(frames)
        group_counts[special_group] = len(frames)
        action_frames.extend(frames)
        action_labels.extend([f"attack {regular_group}, frame {i}" for i in range(len(frames))])

    hit_frames = stage_action_row(action_sheet, 3)
    save_group(hit_frames, battle_dir, 3)
    group_counts[3] = len(hit_frames)
    action_frames.extend(hit_frames)
    action_labels.extend([f"damage, frame {i}" for i in range(len(hit_frames))])

    update_battle_json(creature, battle_json, group_counts, battle_dir)

    short_name = "ultimate" if creature == "dcUltimateDragon" else "absolute"
    save_contact_sheet(
        movement_frames,
        movement_labels,
        SCREENSHOTS / f"{short_name}-dragon-flight-1.5.4.jpg",
    )
    save_contact_sheet(
        action_frames,
        action_labels,
        SCREENSHOTS / f"{short_name}-dragon-actions-1.5.4.jpg",
    )
    save_gif(
        movement_frames,
        SCREENSHOTS / f"{short_name}-dragon-flight-1.5.4.gif",
        [160] * len(movement_frames),
    )
    save_gif(
        action_frames[4:8],
        SCREENSHOTS / f"{short_name}-dragon-attack-1.5.4.gif",
        [180, 150, 260, 220],
    )
    save_gif(
        hit_frames,
        SCREENSHOTS / f"{short_name}-dragon-damage-1.5.4.gif",
        [140, 140, 170, 220],
    )


def main() -> None:
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)

    build_creature(
        "dcUltimateDragon",
        "ultimate-dragon-flight-spritesheet-1.5.4-alpha.png",
        "ultimate-dragon-actions-blackfire-1.5.4-alpha.png",
        {
            20: [(0, "bottom", 285), (1, "bottom", 285), (2, "bottom", 280), (5, "center", 170)],
            0: [(10, "center", 172), (12, "center", 168), (3, "center", 165), (7, "center", 168), (6, "center", 172), (9, "center", 175)],
            21: [(8, "center", 172), (11, "center", 178), (13, "bottom", 280), (14, "bottom", 285)],
        },
    )

    build_creature(
        "dcAbsoluteDragon",
        "absolute-dragon-flight-1.5.4-alpha.png",
        "absolute-dragon-actions-voidfire-1.5.4-alpha.png",
        {
            20: [(0, "bottom", 285), (1, "bottom", 285), (2, "bottom", 280), (3, "center", 170)],
            0: [(4, "center", 170), (5, "center", 166), (6, "center", 164), (7, "center", 168), (8, "center", 172), (9, "center", 176)],
            21: [(10, "center", 170), (11, "center", 176), (12, "center", 180), (13, "bottom", 285)],
        },
    )


if __name__ == "__main__":
    main()
