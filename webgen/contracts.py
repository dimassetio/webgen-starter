"""Kontrak antar modul webgen.

Semua modul (article_gen, framework_gen, logo_gen) harus mengikuti
bentuk data di bawah ini. Jangan diubah tanpa diskusi dengan semua
anggota tim.
"""

from dataclasses import dataclass


@dataclass
class Article:
    """Artikel hasil olahan article_gen (Ifan)."""
    slug: str        # nama file, misal "hello-dunia"
    judul: str       # judul artikel
    html: str        # isi artikel dalam HTML


@dataclass
class FrameworkOutput:
    """Kerangka + tema hasil olahan framework_gen (Arya)."""
    nama_tema: str               # misal "default"
    template_html: str           # kerangka halaman dengan placeholder
    css: str                     # CSS tema
    nav_items: list              # daftar item menu: [{"label": ..., "href": ...}]


@dataclass
class LogoOutput:
    """Logo hasil olahan logo_gen (Faiq)."""
    svg: str                     # isi file SVG logo
    png_path: str                # path file PNG logo
