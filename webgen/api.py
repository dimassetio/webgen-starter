"""API penggabung: menyatukan article_gen, framework_gen, dan logo_gen.

Modul ini dipanggil oleh pemakai webgen. Ia meminta hasil dari tiga
generator, lalu merakitnya menjadi website jadi.
"""

from pathlib import Path

from .contracts import Article, FrameworkOutput, LogoOutput


def generate(
    articles: list,
    framework: FrameworkOutput,
    logo: LogoOutput,
    out_dir: str = "dist",
) -> None:
    """Rakit artikel + kerangka + logo menjadi website di out_dir."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Salin logo ke output
    (out / "logo.svg").write_text(logo.svg)
    (out / "logo.png").write_bytes(Path(logo.png_path).read_bytes())

    # Bangun satu halaman per artikel
    for artikel in articles:
        html = framework.template_html
        html = html.replace("{{LOGO}}", "logo.svg")
        html = html.replace("{{NAV}}", _build_nav(framework.nav_items))
        html = html.replace("{{JUDUL}}", artikel.judul)
        html = html.replace("{{ISI}}", artikel.html)
        (out / f"{artikel.slug}.html").write_text(html)


def _build_nav(items: list) -> str:
    return "".join(
        f'<a href="{item["href"]}">{item["label"]}</a>' for item in items
    )
