"""
Cào FULL cuốn Learning Data Science.
- Nguồn chính: GitHub raw (markdown / notebook gốc)
- Dự phòng: HTML từ learningds.org (không cắt nội dung)
- Output: từng trang + 1 file gom toàn bộ sách
"""

from __future__ import annotations

import html as html_lib
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://learningds.org"
GITHUB_RAW = "https://raw.githubusercontent.com/DS-100/textbook/master/content"
TOC_URL = f"{GITHUB_RAW}/_toc.yml"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "docs" / "book" / "chapters"
HTML_DIR = ROOT / "docs" / "book" / "html"
INDEX_FILE = ROOT / "docs" / "book" / "index.md"
FULL_BOOK_FILE = ROOT / "docs" / "book" / "full_book.md"

DELAY_SEC = 0.25


def fetch(url: str, timeout: int = 60) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (full-book-crawler)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {url}")
        return None
    except Exception as e:
        print(f"  Error: {e} | {url}")
        return None


def file_to_web_url(file_path: str) -> str:
    return f"{BASE_URL}/{file_path.replace('.ipynb', '')}.html"


def file_to_github_url(file_path: str) -> str:
    return f"{GITHUB_RAW}/{file_path}"


def slug_from_path(path: str) -> str:
    return path.replace("/", "_").replace(".ipynb", "")


def parse_toc_paths(yaml_text: str) -> list[str]:
    paths: list[str] = []
    root = re.search(r"^root:\s*(\S+)", yaml_text, re.M)
    if root:
        paths.append(root.group(1))

    for line in yaml_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        m = re.search(r"- file:\s*(.+)", line)
        if m:
            paths.append(m.group(1).strip())
    return paths


def ipynb_to_markdown(raw: str) -> str:
    nb = json.loads(raw)
    parts: list[str] = []
    for cell in nb.get("cells", []):
        src = cell.get("source", [])
        if isinstance(src, list):
            text = "".join(src)
        else:
            text = str(src)
        if not text.strip():
            continue
        ctype = cell.get("cell_type", "")
        if ctype == "markdown":
            parts.append(text.rstrip())
        elif ctype == "code":
            parts.append(f"```python\n{text.rstrip()}\n```")
        else:
            parts.append(text.rstrip())
        parts.append("")
    return "\n".join(parts).strip()


def html_to_markdown(page_html: str) -> tuple[str, str]:
    title_m = re.search(r"<title>([^<]+)</title>", page_html, re.I)
    title = ""
    if title_m:
        title = html_lib.unescape(title_m.group(1)).replace(" — Learning Data Science", "").strip()

    for pattern in (
        r'<article[^>]*class="[^"]*bd-article[^"]*"[^>]*>(.*?)</article>',
        r"<article[^>]*>(.*?)</article>",
        r'<div[^>]*class="[^"]*bd-article-container[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</main>',
        r"<main[^>]*>(.*?)</main>",
    ):
        body_m = re.search(pattern, page_html, re.S | re.I)
        if body_m:
            break
    else:
        return title, ""

    body = body_m.group(1)
    body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.S | re.I)
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.S | re.I)

    # Giữ heading structure
    for lvl in range(6, 0, -1):
        body = re.sub(
            rf"<h{lvl}[^>]*>(.*?)</h{lvl}>",
            lambda m, n=lvl: "\n" + ("#" * n) + " " + html_lib.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() + "\n",
            body,
            flags=re.S | re.I,
        )

    body = re.sub(r"<pre[^>]*><code[^>]*>(.*?)</code></pre>", r"\n```\n\1\n```\n", body, flags=re.S | re.I)
    body = re.sub(r"<li[^>]*>(.*?)</li>", r"\n- \1", body, flags=re.S | re.I)
    body = re.sub(r"<br\s*/?>", "\n", body, flags=re.I)
    body = re.sub(r"<p[^>]*>", "\n\n", body, flags=re.I)
    body = re.sub(r"</p>", "\n", body, flags=re.I)
    body = re.sub(r"<[^>]+>", "", body)
    body = html_lib.unescape(body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    lines = [ln.strip() for ln in body.splitlines()]
    text = "\n".join(ln for ln in lines if ln)
    return title, text


def fetch_page_content(path: str) -> tuple[str, str, str]:
    """Return (title, markdown, source_type)."""
    gh_url = file_to_github_url(path)
    web_url = file_to_web_url(path)

    if path.endswith(".ipynb"):
        raw = fetch(gh_url)
        time.sleep(DELAY_SEC)
        if raw:
            try:
                md = ipynb_to_markdown(raw)
                title = path.split("/")[-1].replace(".ipynb", "").replace("_", " ").title()
                return title, md, "github-ipynb"
            except json.JSONDecodeError:
                pass
    else:
        raw = fetch(gh_url)
        time.sleep(DELAY_SEC)
        if raw and raw.strip():
            title = path.split("/")[-1].replace("_", " ").title()
            if path == "intro":
                title = "Introduction"
            elif path == "preface":
                title = "Preface"
            return title, raw.strip(), "github-md"

    page_html = fetch(web_url)
    time.sleep(DELAY_SEC)
    if page_html:
        HTML_DIR.mkdir(parents=True, exist_ok=True)
        (HTML_DIR / f"{slug_from_path(path)}.html").write_text(page_html, encoding="utf-8")
        title, md = html_to_markdown(page_html)
        return title or path, md, "web-html"

    return path, "", "fail"


def main():
    print("Fetching _toc.yml...")
    toc_yaml = fetch(TOC_URL)
    if not toc_yaml:
        raise SystemExit("Failed to fetch _toc.yml")

    paths = parse_toc_paths(toc_yaml)
    print(f"Found {len(paths)} pages.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    book_parts: list[str] = [
        "# Learning Data Science — Full Book (offline copy)",
        "",
        "Nguồn: [learningds.org](https://learningds.org/intro.html) | "
        "[GitHub DS-100/textbook](https://github.com/DS-100/textbook)",
        "",
        "---",
        "",
    ]
    ok, fail = 0, 0
    total_chars = 0

    for i, path in enumerate(paths, 1):
        print(f"[{i}/{len(paths)}] {path}")
        title, content, source = fetch_page_content(path)

        if not content:
            fail += 1
            results.append({
                "path": path,
                "url": file_to_web_url(path),
                "title": title,
                "status": "fail",
                "source": source,
                "chars": 0,
            })
            continue

        ok += 1
        total_chars += len(content)
        web_url = file_to_web_url(path)
        out_file = OUTPUT_DIR / f"{slug_from_path(path)}.md"
        out_file.write_text(
            f"# {title}\n\n"
            f"**Nguồn web:** [{web_url}]({web_url})  \n"
            f"**Nguồn tải:** `{source}` | `{path}`\n\n"
            f"---\n\n{content}\n",
            encoding="utf-8",
        )

        book_parts.extend([
            f"## {title}",
            "",
            f"> File: `{path}` | Nguồn: {source}",
            "",
            content,
            "",
            "---",
            "",
        ])

        results.append({
            "path": path,
            "url": web_url,
            "title": title,
            "status": "ok",
            "source": source,
            "chars": len(content),
            "preview": content[:300].replace("\n", " "),
        })

    FULL_BOOK_FILE.write_text("\n".join(book_parts), encoding="utf-8")

    lines = [
        "# Learning Data Science — Mục lục (FULL)",
        "",
        "Cuốn sách: [Learning Data Science](https://learningds.org/intro.html).",
        "",
        f"**Kết quả:** {ok}/{len(paths)} trang | {total_chars:,} ký tự | {fail} lỗi",
        f"**Từng trang:** `docs/book/chapters/`",
        f"**Gom full sách:** `docs/book/full_book.md`",
        f"**HTML dự phòng:** `docs/book/html/`",
        "",
        "---",
        "",
    ]
    for item in results:
        icon = "✅" if item["status"] == "ok" else "❌"
        extra = f" ({item['chars']:,} chars, {item.get('source', '')})" if item["status"] == "ok" else ""
        lines.append(f"- {icon} [{item['title']}]({item['url']}) — `{item['path']}`{extra}")

    INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")
    meta = {
        "total": len(paths),
        "ok": ok,
        "fail": fail,
        "total_chars": total_chars,
        "full_book": str(FULL_BOOK_FILE),
        "pages": results,
    }
    (OUTPUT_DIR / "_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nDone! {ok}/{len(paths)} pages, {total_chars:,} chars")
    print(f"Full book: {FULL_BOOK_FILE}")
    print(f"Index: {INDEX_FILE}")


if __name__ == "__main__":
    main()
