"""Generate favicon + social preview for fullstackcv/playbook."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent

# Palette matching the MkDocs Material indigo + amber theme.
INDIGO = (48, 63, 159)          # Material Indigo 700
INDIGO_DARK = (26, 35, 126)     # Material Indigo 900
AMBER = (255, 193, 7)           # Material Amber 500
AMBER_DIM = (255, 193, 7, 180)  # amber with alpha
OFFWHITE = (236, 239, 241)      # Material Blue Grey 50
MUTED = (176, 190, 197)         # Material Blue Grey 200


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        f"/System/Library/Fonts/Supplemental/{name}",
        f"/System/Library/Fonts/{name}",
        f"/Library/Fonts/{name}",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    # Fallback: Helvetica ttc
    return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)


def make_favicon(size: int, out_path: Path) -> None:
    img = Image.new("RGBA", (size, size), INDIGO + (255,))
    draw = ImageDraw.Draw(img)
    # Three amber bars (representing 3 picks)
    pad = max(size // 6, 2)
    bar_h = max(size // 10, 2)
    gap = max(size // 12, 1)
    # Center three bars vertically
    total_h = bar_h * 3 + gap * 2
    y0 = (size - total_h) // 2
    for i in range(3):
        y = y0 + i * (bar_h + gap)
        # vary width slightly for visual interest
        widths = [0.75, 0.85, 0.65]
        bar_w = int((size - 2 * pad) * widths[i])
        draw.rounded_rectangle(
            [(pad, y), (pad + bar_w, y + bar_h)],
            radius=max(bar_h // 2, 1),
            fill=AMBER + (255,),
        )
    img.save(out_path, optimize=True)
    print(f"Wrote {out_path.name} ({size}x{size})")


def make_social_preview(out_path: Path) -> None:
    W, H = 1280, 640
    img = Image.new("RGBA", (W, H), INDIGO_DARK + (255,))
    draw = ImageDraw.Draw(img)

    # Subtle gradient: draw a lighter indigo radial glow in top-left
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for i in range(40, 0, -1):
        alpha = int(i * 1.5)
        glow_draw.ellipse(
            [(-300 - i * 10, -200 - i * 10), (600 + i * 10, 500 + i * 10)],
            fill=(63, 81, 181, alpha),
        )
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # Three amber bars left side (conveys "three picks")
    bar_left = 80
    bar_top = 160
    bar_h = 18
    bar_gap = 20
    widths = [360, 440, 280]
    alphas = [255, 210, 150]
    for i, (w, a) in enumerate(zip(widths, alphas)):
        y = bar_top + i * (bar_h + bar_gap)
        draw.rounded_rectangle(
            [(bar_left, y), (bar_left + w, y + bar_h)],
            radius=bar_h // 2,
            fill=AMBER + (a,),
        )

    # Title
    title_font = load_font("Helvetica.ttc", 88)
    tagline_font = load_font("Helvetica.ttc", 40)
    sub_font = load_font("Helvetica.ttc", 30)

    try:
        # Prefer bold if the face supports variant selection
        bold_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 88, index=1)
    except Exception:
        bold_font = title_font

    # Title
    draw.text((80, 330), "fullstackcv / playbook", font=bold_font, fill=(255, 255, 255, 255))
    # Tagline (amber)
    draw.text((80, 440), "Opinionated CV reference", font=tagline_font, fill=AMBER + (255,))
    # Subtitle (muted)
    draw.text(
        (80, 498),
        "Three picks per subtask, not 600.",
        font=sub_font,
        fill=MUTED + (255,),
    )

    # GitHub URL bottom-right
    url_font = load_font("Helvetica.ttc", 24)
    url = "fullstackcv.github.io/playbook"
    bbox = draw.textbbox((0, 0), url, font=url_font)
    url_w = bbox[2] - bbox[0]
    draw.text(
        (W - url_w - 80, H - 48),
        url,
        font=url_font,
        fill=MUTED + (230,),
    )

    # Flatten to RGB
    final = Image.new("RGB", (W, H), INDIGO_DARK)
    final.paste(img, (0, 0), img)
    final.save(out_path, optimize=True)
    print(f"Wrote {out_path.name} ({W}x{H})")


if __name__ == "__main__":
    make_favicon(32, OUT / "favicon.png")
    make_favicon(64, OUT / "favicon-64.png")
    make_favicon(192, OUT / "favicon-192.png")
    make_social_preview(OUT / "social-preview.png")
