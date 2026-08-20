"""Contoh penggunaan article_gen.

Jalankan:
    python -m article_gen.example
"""

from article_gen import markdown_to_html, render_article, render_articles


def main() -> None:
    articles = render_articles("Hello Dunia", "# Halo\nIsi **bold** dan [link](https://example.com)")
    print(f"Jumlah artikel: {len(articles)}")
    for art in articles:
        print(f"- slug={art.slug} judul={art.judul}")
        print(art.html[:160], "...")
        print()

    html = markdown_to_html("## Judul\n- satu\n- dua\n\nParagraf *miring*")
    print("markdown_to_html demo:\n", html[:200])

    single = render_article("Judul Baru", "Isi **tebal**")
    print("\nrender_article:", single.slug, single.judul)


if __name__ == "__main__":
    main()
