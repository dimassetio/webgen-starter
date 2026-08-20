"""framework_gen — Kerangka + Tema (Arya).

Menyediakan template HTML, navigasi/menu, dan sistem tema.
Output mengikuti kontrak webgen/contracts.py -> FrameworkOutput.

Pemakaian:
    from framework_gen import get_framework, render, get_themes

    fw = get_framework(theme="default")
    # atau langsung render halaman jadi:
    html = render("Hello Dunia", "<p>Isi artikel</p>", logo="logo.svg", theme="dark")

Placeholder yang didukung template (kompatibel dengan webgen/api.py):
    {{LOGO}}  -> path logo (logo.svg)
    {{NAV}}   -> HTML navigasi (dibangun dari nav_items)
    {{JUDUL}} -> judul artikel
    {{ISI}}   -> isi HTML artikel
    {{CSS}}   -> sudah di-inline ke <style> saat get_framework(), tidak perlu di-replace lagi

Tema bawaan: default, dark, minimal, modern
"""

from webgen.contracts import FrameworkOutput

NAV_DEFAULT = [
    {"label": "Beranda", "href": "index.html"},
    {"label": "Artikel", "href": "artikel.html"},
    {"label": "Tentang", "href": "tentang.html"},
]

CSS_DEFAULT = r"""
:root{--bg:#f8fafc;--card:#ffffff;--text:#0f172a;--muted:#64748b;--primary:#2563eb;--border:#e2e8f0;--radius:14px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial;background:var(--bg);color:var(--text);line-height:1.7}
a{color:var(--primary);text-decoration:none}a:hover{text-decoration:underline}
header{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.85);backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}
.header-inner{max-width:1100px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{display:flex;align-items:center;gap:12px;font-weight:700}
.brand img{width:36px;height:36px;object-fit:contain}
nav{display:flex;gap:14px;flex-wrap:wrap}
nav a{padding:8px 12px;border-radius:999px;font-weight:500;color:var(--text)}
nav a:hover{background:var(--bg);text-decoration:none}
main{max-width:1100px;margin:28px auto;padding:0 20px}
.hero{background:linear-gradient(135deg,#2563eb 0%, #7c3aed 100%);color:white;border-radius:var(--radius);padding:36px 28px;margin-bottom:22px}
.hero h1{margin:0 0 8px;font-size:28px;line-height:1.2}
.hero p{margin:0;opacity:.9}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:22px;box-shadow:0 4px 20px rgba(15,23,42,.04)}
article h1,article h2,article h3{line-height:1.25}
article h2{margin-top:28px;border-bottom:1px solid var(--border);padding-bottom:8px}
article p{color:#1e293b}
article blockquote{border-left:4px solid var(--primary);margin:18px 0;padding:10px 16px;background:#eff6ff;border-radius:8px;color:#1e40af}
article pre{background:#0f172a;color:#e2e8f0;padding:16px;border-radius:10px;overflow:auto}
article code{background:#f1f5f9;padding:2px 6px;border-radius:6px;font-size:.9em}
article table{width:100%;border-collapse:collapse;margin:16px 0}
article th,article td{border:1px solid var(--border);padding:8px 10px;text-align:left}
article th{background:#f8fafc}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
footer{max-width:1100px;margin:30px auto;padding:16px 20px;color:var(--muted);text-align:center;border-top:1px solid var(--border)}
@media(max-width:640px){.header-inner{flex-direction:column;align-items:flex-start} .hero h1{font-size:22px}}
"""

CSS_DARK = r"""
:root{--bg:#0b1220;--card:#121a2b;--text:#e2e8f0;--muted:#94a3b8;--primary:#60a5fa;--border:#1e293b;--radius:14px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Inter,ui-sans-serif,system-ui;background:var(--bg);color:var(--text);line-height:1.7}
a{color:var(--primary);text-decoration:none}a:hover{text-decoration:underline}
header{position:sticky;top:0;z-index:20;background:rgba(18,26,43,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}
.header-inner{max-width:1100px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{display:flex;align-items:center;gap:12px;font-weight:700;color:var(--text)}
.brand img{width:36px;height:36px}
nav{display:flex;gap:10px;flex-wrap:wrap}
nav a{padding:8px 12px;border-radius:999px;color:var(--text);border:1px solid transparent}
nav a:hover{background:#1e293b;border-color:var(--border);text-decoration:none}
main{max-width:1100px;margin:28px auto;padding:0 20px}
.hero{background:linear-gradient(135deg,#1e3a8a 0%, #312e81 100%);color:white;border-radius:var(--radius);padding:36px 28px;margin-bottom:22px;border:1px solid var(--border)}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:22px}
article h2{border-bottom:1px solid var(--border);padding-bottom:8px}
article p{color:#cbd5e1}
article blockquote{border-left:4px solid var(--primary);background:#0f172a;color:#93c5fd;padding:10px 16px;border-radius:8px}
article pre{background:#020617;color:#e2e8f0;padding:16px;border-radius:10px;overflow:auto;border:1px solid var(--border)}
article code{background:#1e293b;padding:2px 6px;border-radius:6px}
footer{max-width:1100px;margin:30px auto;padding:16px 20px;color:var(--muted);text-align:center;border-top:1px solid var(--border)}
"""

CSS_MINIMAL = r"""
:root{--bg:#ffffff;--text:#1a1a1a;--muted:#6b7280;--primary:#111827;--border:#e5e7eb;--radius:8px}
*{box-sizing:border-box}
body{margin:0;font-family:Georgia,'Times New Roman',serif;background:var(--bg);color:var(--text);line-height:1.8}
a{color:var(--primary);text-decoration:underline;text-underline-offset:3px}
header{border-bottom:1px solid var(--border);background:white}
.header-inner{max-width:720px;margin:0 auto;padding:18px 20px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{font-family:Inter,system-ui,sans-serif;font-weight:800;letter-spacing:-.02em;display:flex;align-items:center;gap:10px}
.brand img{width:32px;height:32px}
nav{display:flex;gap:18px;font-family:Inter,system-ui,sans-serif;font-size:14px}
nav a{text-decoration:none;color:var(--muted)}nav a:hover{color:var(--text)}
main{max-width:720px;margin:32px auto;padding:0 20px}
.card{padding:0;border:none;background:transparent}
article h1{font-family:Inter,system-ui,sans-serif;font-size:32px;letter-spacing:-.02em;margin-bottom:8px}
article h2{font-family:Inter,system-ui,sans-serif;margin-top:32px}
article p{font-size:17px}
article blockquote{border-left:3px solid var(--text);margin:20px 0;padding:8px 18px;font-style:italic;background:#f9fafb}
footer{max-width:720px;margin:40px auto;padding:16px 20px;color:var(--muted);text-align:center;border-top:1px solid var(--border);font-family:Inter,system-ui,sans-serif;font-size:13px}
"""

CSS_MODERN = r"""
:root{--bg:#f5f5f7;--card:#ffffff;--text:#1d1d1f;--muted:#6e6e73;--primary:#0071e3;--border:#d2d2d7;--radius:18px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:'SF Pro Display',Inter,system-ui,-apple-system;background:var(--bg);color:var(--text);line-height:1.6}
a{color:var(--primary);text-decoration:none}a:hover{text-decoration:underline}
header{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.8);backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid var(--border)}
.header-inner{max-width:1100px;margin:0 auto;padding:14px 22px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:12px;font-weight:700;letter-spacing:-.02em}
.brand img{width:34px;height:34px;border-radius:8px}
nav{display:flex;gap:8px}
nav a{padding:8px 14px;border-radius:999px;background:white;border:1px solid var(--border);font-size:14px;font-weight:500;color:var(--text)}
nav a:hover{background:var(--text);color:white;border-color:var(--text);text-decoration:none}
main{max-width:1100px;margin:26px auto;padding:0 22px}
.hero{background:white;border:1px solid var(--border);border-radius:var(--radius);padding:40px 30px;margin-bottom:20px}
.hero h1{margin:0 0 8px;font-size:32px;letter-spacing:-.03em}
.hero p{margin:0;color:var(--muted);font-size:17px}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px;box-shadow:0 8px 30px rgba(0,0,0,.04)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
article pre{background:#1d1d1f;color:white;padding:16px;border-radius:12px;overflow:auto}
footer{max-width:1100px;margin:30px auto;padding:16px 22px;color:var(--muted);text-align:center;font-size:13px}
"""

THEMES = {
    "default": CSS_DEFAULT,
    "dark": CSS_DARK,
    "minimal": CSS_MINIMAL,
    "modern": CSS_MODERN,
}

BASE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{JUDUL}} - WebGen</title>
<meta name="description" content="{{JUDUL}}">
<style>{{CSS}}</style>
</head>
<body>
<header>
  <div class="header-inner">
    <a class="brand" href="index.html">
      <img src="{{LOGO}}" alt="Logo">
      <span>WebGen</span>
    </a>
    <nav>{{NAV}}</nav>
  </div>
</header>
<main>
  <div class="hero">
    <h1>{{JUDUL}}</h1>
    <p>Generated by WebGen — framework_gen (Arya)</p>
  </div>
  <div class="card">
    <article>
      {{ISI}}
    </article>
  </div>
</main>
<footer>
  <p>&copy; 2026 WebGen &middot; Dibuat dengan framework_gen &middot; Tema: {{TEMA}}</p>
</footer>
</body>
</html>
"""


def _build_nav(items: list) -> str:
    if not items:
        return ""
    return "".join(f'<a href="{it["href"]}">{it["label"]}</a>' for it in items)


def get_themes() -> list:
    return list(THEMES.keys())


def get_css(theme: str = "default") -> str:
    if theme not in THEMES:
        raise ValueError(f"Tema '{theme}' tidak ditemukan. Pilihan: {', '.join(THEMES)}")
    return THEMES[theme]


def get_template(theme: str = "default") -> str:
    css = get_css(theme)
    html = BASE_TEMPLATE.replace("{{CSS}}", css).replace("{{TEMA}}", theme)
    return html


def get_framework(theme: str = "default", nav_items: list | None = None) -> FrameworkOutput:
    css = get_css(theme)
    template = BASE_TEMPLATE.replace("{{CSS}}", css).replace("{{TEMA}}", theme)
    nav = nav_items if nav_items is not None else list(NAV_DEFAULT)
    return FrameworkOutput(
        nama_tema=theme,
        template_html=template,
        css=css,
        nav_items=nav,
    )


def render(judul: str, isi_html: str, logo: str = "logo.svg", theme: str = "default", nav_items: list | None = None) -> str:
    fw = get_framework(theme=theme, nav_items=nav_items)
    html = fw.template_html
    html = html.replace("{{LOGO}}", logo)
    html = html.replace("{{NAV}}", _build_nav(fw.nav_items))
    html = html.replace("{{JUDUL}}", judul)
    html = html.replace("{{ISI}}", isi_html)
    return html


def render_page(judul: str, isi_html: str, logo: str = "logo.svg", theme: str = "default", nav_items: list | None = None) -> str:
    return render(judul, isi_html, logo=logo, theme=theme, nav_items=nav_items)


__all__ = [
    "FrameworkOutput",
    "THEMES",
    "NAV_DEFAULT",
    "BASE_TEMPLATE",
    "get_themes",
    "get_css",
    "get_template",
    "get_framework",
    "render",
    "render_page",
]
