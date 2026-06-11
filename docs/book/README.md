# Learning Data Science (offline)

Bản crawl cuốn [Learning Data Science](https://learningds.org/intro.html) (DS-100 / textbook).

| File / thư mục | Mô tả |
|----------------|--------|
| [`index.md`](index.md) | Mục lục đầy đủ 150 trang, link gốc |
| [`full_book.md`](full_book.md) | Gom toàn bộ sách một file (~976k ký tự) |
| [`chapters/`](chapters/) | Từng trang / mục riêng (`ch_*.md`, …) |
| [`chapters/_meta.json`](chapters/_meta.json) | Metadata crawl (ngày, số trang, preview) |

**Crawl lại:** `python scripts/crawl_learningds.py` (output ghi vào `chapters/`, `index.md`, `full_book.md`).
