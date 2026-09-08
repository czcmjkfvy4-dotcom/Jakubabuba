from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
SOURCE = ASSETS / "installer-key-art.png"


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as source:
        art = source.convert("RGB")

    wizard = ImageOps.fit(art, (164, 314), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    wizard.save(ASSETS / "wizard.bmp")

    small = ImageOps.fit(art, (55, 55), method=Image.Resampling.LANCZOS, centering=(0.5, 0.58))
    small.save(ASSETS / "wizard-small.bmp")

    icon_source = ImageOps.fit(art, (256, 256), method=Image.Resampling.LANCZOS, centering=(0.5, 0.64))
    icon_source.save(
        ASSETS / "dragon-citadel.ico",
        sizes=((16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)),
    )


if __name__ == "__main__":
    main()
