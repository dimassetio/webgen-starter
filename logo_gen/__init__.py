"""logo_gen — Pembuat Logo (Faiq).

Menghasilkan logo WebGen (SVG + PNG) sesuai kontrak
webgen/contracts.py -> LogoOutput.

Output:
    LogoOutput(svg: str, png_path: str)

Pemakaian:
    from logo_gen import render_logo, get_logo_path

    logo = render_logo(size=512)
    # logo.svg -> string SVG
    # logo.png_path -> path file PNG (logo_gen/logo-512.png)

    # atau hanya path:
    path = get_logo_path(1024)

PNG di-generate otomatis (fallback Pillow) dan di-cache di
folder logo_gen/ sebagai logo.png / logo-{size}.png.
SVG bersifat deterministik (WG monogram).
"""

from pathlib import Path

from webgen.contracts import LogoOutput

_LOGO_DIR = Path(__file__).parent
_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="WebGen WG logo">
  <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2463EB"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient></defs>
  <circle cx="512" cy="512" r="420" fill="url(#g)"/>
  <circle cx="512" cy="512" r="406" fill="none" stroke="white" stroke-opacity="0.35" stroke-width="6"/>
  <text x="512" y="570" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-weight="700" font-size="420" fill="white">WG</text>
  <text x="512" y="748" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-weight="700" font-size="78" fill="white" opacity="0.82" letter-spacing="18">WEBGEN</text>
</svg>"""


def _ensure_png(size: int = 1024) -> Path:
    name = "logo.png" if size == 1024 else f"logo-{size}.png"
    p = _LOGO_DIR / name
    if not p.exists():
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx, cy, r = size // 2, size // 2, int(420 * size / 1024)
        for i in range(r, 0, -1):
            t = i / r
            c1, c2 = (36, 99, 235), (79, 70, 229)
            col = tuple(int(c1[k] * t + c2[k] * (1 - t)) for k in range(3)) + (255,)
            d.ellipse([cx - i, cy - i, cx + i, cy + i], fill=col)
        d.ellipse(
            [cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3],
            outline=(255, 255, 255, 90),
            width=max(1, 6 * size // 1024),
        )
        fp = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        try:
            fb = ImageFont.truetype(fp, int(420 * size / 1024))
            fs = ImageFont.truetype(fp, int(78 * size / 1024))
        except Exception:
            fb = ImageFont.load_default()
            fs = ImageFont.load_default()
        tw_box = d.textbbox((0, 0), "WG", font=fb)
        tw, th = tw_box[2] - tw_box[0], tw_box[3] - tw_box[1]
        tx, ty = (size - tw) // 2 - 2 * size // 1024, (size - th) // 2 - 46 * size // 1024
        d.text((tx + 3 * size // 1024, ty + 4 * size // 1024), "WG", fill=(0, 0, 0, 55), font=fb)
        d.text((tx, ty), "WG", fill=(255, 255, 255, 255), font=fb)
        sub = "WEBGEN"
        tw2 = d.textbbox((0, 0), sub, font=fs)[2]
        d.text(((size - tw2) // 2, cy + 210 * size // 1024), sub, fill=(255, 255, 255, 210), font=fs)
        img.save(p, "PNG")
    return p


def render_logo(size: int = 1024) -> LogoOutput:
    """Hasilkan logo sesuai kontrak LogoOutput (svg + png_path)."""
    png = _ensure_png(size)
    return LogoOutput(svg=_SVG, png_path=str(png))


def get_logo_path(size: int = 1024) -> str:
    return str(_ensure_png(size))


__all__ = ["LogoOutput", "render_logo", "get_logo_path"]
