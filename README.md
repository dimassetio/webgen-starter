# WebGen

Generator website modular. Dibangun dari 3 generator terpisah yang digabungkan menjadi satu library Python.

```
article_gen    →  framework_gen  →  logo_gen
(artikel)         (kerangka+tema)   (logo)
        \             |            /
         \            v           /
          └───────  webgen  ──────┘
          (API penggabung: hasilnya website jadi)
```

## Pembagian tugas

| Bagian | Modul | Folder | Penanggung jawab |
|--------|-------|--------|------------------|
| Artikel generator | `article_gen` | `article_gen/` | Ifan |
| Kerangka & tema generator | `framework_gen` | `framework_gen/` | Arya |
| Logo generator | `logo_gen` | `logo_gen/` | Faiq |
| API penggabung & kontrak | `webgen` | `webgen/` | Pemilik repo |

## Tugas masing-masing

### Ifan — `article_gen/`
- Buat modul yang mengubah input artikel (judul, isi) menjadi HTML artikel.
- Hasil keluarannya harus berbentuk: `{"slug": "...", "judul": "...", "html": "..."}` per artikel, atau list of dict.
- Lihat `webgen/contracts.py` — ikuti bentuk data di sana.
- Contoh pemakaian yang harus didukung:
  ```python
  from article_gen import render_articles
  articles = render_articles("judul", "isi markdown")
  ```

### Arya — `framework_gen/`
- Buat modul kerangka (template HTML, navigasi/menu) + sistem tema.
- Hasil keluarannya harus menyediakan fungsi render yang menerima konten dan logo, lalu menghasilkan halaman HTML utuh.
- Bisa lebih dari satu tema; tentukan tema aktif lewat parameter.
- Ikuti `webgen/contracts.py`.

### Faiq — `logo_gen/`
- Buat modul pembuat logo (SVG/PNG).
- Hasil keluarannya: file logo + path/nama file standar agar bisa dipakai framework.
- Ikuti `webgen/contracts.py`.

### Pemilik repo — `webgen/`
- `contracts.py`: kontrak antar modul (jangan diubah tanpa koordinasi).
- `api.py`: menyatukan hasil 3 modul menjadi output final.
- `__init__.py`: API publik `webgen.generate(...)`.

## Aturan main

1. Hanya kerjakan modul sesuai tugasmu di atas.
2. `webgen/contracts.py` adalah kontrak — kalau butuh mengubahnya, diskusikan dulu dengan semua.
3. Semua modul adalah library Python (dipanggil via `import`), bukan script yang langsung dijalankan.
4. Nama fungsi dan bentuk data mengikuti `contracts.py`.

## Cara menjalankan (contoh)

```python
from webgen import generate

generate()
# → menghasilkan website jadi di folder dist/
```

## Status pengerjaan

- [ ] `article_gen/` — Ifan
- [ ] `framework_gen/` — Arya
- [ ] `logo_gen/` — Faiq
- [ ] `webgen/` (API penggabung) — pemilik repo
