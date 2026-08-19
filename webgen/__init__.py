"""WebGen: API penggabung dan kontrak antar modul."""

from .api import generate
from .contracts import Article, FrameworkOutput, LogoOutput

__all__ = ["generate", "Article", "FrameworkOutput", "LogoOutput"]
