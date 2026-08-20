"""article_gen — Generator Artikel (Ifan).

Mengubah input judul + isi markdown menjadi HTML artikel.
Output mengikuti kontrak webgen/contracts.py -> Article.

Pemakaian sesuai README:
    from article_gen import render_articles
    articles = render_articles("Hello Dunia", "# Halo\\nIsi **bold**")
    # -> [Article(slug="hello-dunia", judul="Hello Dunia", html="<h1>Halo</h1>...")]

Mendukung juga:
    from article_gen import render_article, markdown_to_html, slugify

    html = markdown_to_html("# Judul\\nParagraf **tebal**")
    art = render_article("Judul", "isi markdown")
"""

from __future__ import annotations

import html as html_lib
import re

from webgen.contracts import Article


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")[:60] or "artikel"


def _escape(text: str) -> str:
    return html_lib.escape(text, quote=False)


def _inline(md: str) -> str:
    md = html_lib.escape(md, quote=False)
    md = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" style="max-width:100%;height:auto">', md)
    md = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', md)
    md = re.sub(r"`([^`]+?)`", r"<code>\1</code>", md)
    md = re.sub(r"\*\*([^*]+?)\*\*", r"<strong>\1</strong>", md)
    md = re.sub(r"__([^_]+?)__", r"<strong>\1</strong>", md)
    md = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", md)
    md = re.sub(r"_([^_]+?)_", r"<em>\1</em>", md)
    return md


def markdown_to_html(md: str) -> str:
    if not md or not md.strip():
        return ""
    md = md.replace("\r\n", "\n")
    code_blocks: dict[str, str] = {}

    def _save_code(m: re.Match) -> str:
        lang = (m.group(1) or "").strip()
        code = html_lib.escape(m.group(2))
        key = f"__CODEBLOCK_{len(code_blocks)}__"
        cls = f' class="language-{_escape(lang)}"' if lang else ""
        code_blocks[key] = f"<pre><code{cls}>{code}</code></pre>"
        return key

    md = re.sub(r"```(\w*)\n([\s\S]*?)```", _save_code, md)
    lines = md.split("\n")
    out: list[str] = []
    i = 0
    in_ul = False
    in_ol = False
    in_blockquote: list[str] = []
    para_buf: list[str] = []

    def _flush_para() -> None:
        nonlocal para_buf
        if para_buf:
            text = " ".join(para_buf).strip()
            if text:
                if text.startswith("__CODEBLOCK_"):
                    out.append(code_blocks.get(text, text))
                else:
                    out.append(f"<p>{_inline(text)}</p>")
            para_buf = []

    def _close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def _flush_blockquote() -> None:
        nonlocal in_blockquote
        if in_blockquote:
            inner = " ".join(in_blockquote).strip()
            out.append(f"<blockquote><p>{_inline(inner)}</p></blockquote>")
            in_blockquote = []

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if line.startswith("__CODEBLOCK_") and line in code_blocks:
            _flush_para()
            _flush_blockquote()
            _close_lists()
            out.append(code_blocks[line])
            i += 1
            continue
        if not line:
            _flush_para()
            _flush_blockquote()
            _close_lists()
            i += 1
            continue
        if re.match(r"^---+ *$", line) or re.match(r"^\*\*\*+ *$", line) or re.match(r"^___+ *$", line):
            _flush_para()
            _flush_blockquote()
            _close_lists()
            out.append("<hr>")
            i += 1
            continue
        m_h = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m_h:
            _flush_para()
            _flush_blockquote()
            _close_lists()
            level = len(m_h.group(1))
            title = _inline(m_h.group(2).strip())
            out.append(f"<h{level}>{title}</h{level}>")
            i += 1
            continue
        if line.startswith(">"):
            _flush_para()
            _close_lists()
            in_blockquote.append(line.lstrip("> ").strip())
            if i + 1 >= len(lines) or not lines[i + 1].strip().startswith(">"):
                _flush_blockquote()
            i += 1
            continue
        else:
            if in_blockquote:
                _flush_blockquote()
        m_ul = re.match(r"^[-*]\s+(.+)$", line)
        if m_ul:
            _flush_para()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{_inline(m_ul.group(1).strip())}</li>")
            if i + 1 >= len(lines) or not re.match(r"^[-*]\s+", lines[i + 1].strip()):
                out.append("</ul>")
                in_ul = False
            i += 1
            continue
        m_ol = re.match(r"^\d+\.\s+(.+)$", line)
        if m_ol:
            _flush_para()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{_inline(m_ol.group(1).strip())}</li>")
            if i + 1 >= len(lines) or not re.match(r"^\d+\.\s+", lines[i + 1].strip()):
                out.append("</ol>")
                in_ol = False
            i += 1
            continue
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|[\s:|:-]*$", lines[i + 1]):
            _flush_para()
            _close_lists()
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            out.append("<table>")
            out.append("<thead><tr>" + "".join(f"<th>{_inline(h)}</th>" for h in headers) + "</tr></thead>")
            out.append("<tbody>")
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue
        para_buf.append(raw.strip())
        i += 1
    _flush_para()
    _flush_blockquote()
    _close_lists()
    html_out = "\n".join(out)
    for k, v in code_blocks.items():
        if k in html_out:
            html_out = html_out.replace(f"<p>{k}</p>", v)
    return html_out


def render_article(judul: str, isi_markdown: str) -> Article:
    slug = slugify(judul)
    html_content = markdown_to_html(isi_markdown)
    return Article(slug=slug, judul=judul, html=html_content)


def render_articles(*args, **kwargs) -> list[Article]:
    if len(args) == 1 and isinstance(args[0], list):
        items = args[0]
        result: list[Article] = []
        seen: set[str] = set()
        for entry in items:
            if isinstance(entry, (list, tuple)) and len(entry) == 2:
                judul, isi = str(entry[0]), str(entry[1])
            elif isinstance(entry, dict):
                judul = str(entry.get("judul") or entry.get("title") or "")
                isi = str(entry.get("isi") or entry.get("body") or entry.get("markdown") or entry.get("content") or "")
            else:
                continue
            art = render_article(judul, isi)
            base, n = art.slug, 2
            while art.slug in seen:
                art.slug = f"{base}-{n}"
                n += 1
            seen.add(art.slug)
            result.append(art)
        return result
    if len(args) == 2:
        judul, isi = str(args[0]), str(args[1])
        return [render_article(judul, isi)]
    if "judul" in kwargs and "isi" in kwargs:
        return [render_article(str(kwargs["judul"]), str(kwargs["isi"]))]
    if "title" in kwargs and "markdown" in kwargs:
        return [render_article(str(kwargs["title"]), str(kwargs["markdown"]))]
    if args and isinstance(args[0], str) and kwargs.get("isi_markdown"):
        return [render_article(str(args[0]), str(kwargs["isi_markdown"]))]
    raise TypeError("render_articles(judul, isi_markdown) atau render_articles([(judul, isi), ...])")


__all__ = ["Article", "slugify", "markdown_to_html", "render_article", "render_articles"]
