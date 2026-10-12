"""Build everything that gets uploaded to WordPress.

    python3 tools/build.py

Outputs
    elementor/<slug>.json             one Elementor template per page (Templates > Import)
    import/schnitzmenu-pages.xml      all pages in one WordPress import file (Tools > Import > WordPress)
    dist/astra-child-schnitzmenu.zip  the child theme (Appearance > Themes > Upload)
    dist/elementor-templates.zip      every Elementor template in one upload
"""
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from elementor import reset_ids, walk  # noqa: E402
from pages import PAGES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
THEME = ROOT / "astra-child-schnitzmenu"
ELEMENTOR_VERSION = "3.25.0"


def check_safe(slug, payload):
    """The WordPress importer unslashes meta values, so the JSON must not contain backslashes."""
    if "\\" in payload:
        idx = payload.index("\\")
        raise SystemExit(f"{slug}: backslash in Elementor JSON near: {payload[max(0, idx - 60):idx + 20]}")
    if "]]>" in payload:
        raise SystemExit(f"{slug}: ']]>' would break the CDATA block")


def fallback_html(elements):
    """Plain HTML copy for post_content (used by SEO plugins and if Elementor is ever switched off)."""
    out = []
    for el in walk(elements):
        if el["elType"] != "widget":
            continue
        s = el["settings"]
        kind = el["widgetType"]
        if kind == "heading":
            tag = s.get("header_size", "h2")
            out.append(f"<{tag}>{s['title']}</{tag}>")
        elif kind == "text-editor":
            out.append(s["editor"])
        elif kind == "shortcode":
            out.append(s["shortcode"])
        elif kind == "button":
            out.append(f"<p><a href='{s['link']['url']}'>{s['text']}</a></p>")
    return "\n".join(out)


def meta(key, value):
    return (f"\t\t<wp:postmeta>\n\t\t\t<wp:meta_key><![CDATA[{key}]]></wp:meta_key>\n"
            f"\t\t\t<wp:meta_value><![CDATA[{value}]]></wp:meta_value>\n\t\t</wp:postmeta>\n")


def words(html):
    return len(re.sub(r"<[^>]+>|\[[^\]]+\]|&#?\w+;", " ", html).split())


def main():
    (ROOT / "elementor").mkdir(exist_ok=True)
    (ROOT / "import").mkdir(exist_ok=True)
    (ROOT / "dist").mkdir(exist_ok=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    items = []
    report = []

    for i, (slug, title, seo_title, seo_desc, builder, template, sidebar) in enumerate(PAGES):
        reset_ids(slug)
        content = builder()
        data = json.dumps(content, ensure_ascii=False, separators=(",", ":"))
        check_safe(slug, data)

        template_json = {
            "version": "0.4",
            "title": f"SchnitzMenu - {title}",
            "type": "page",
            "page_settings": {"hide_title": "yes"},
            "content": content,
        }
        (ROOT / "elementor" / f"{slug}.json").write_text(
            json.dumps(template_json, ensure_ascii=False, indent=1), encoding="utf-8")

        body = fallback_html(content)
        report.append((slug, words(body)))
        focus = seo_title.split(" - ")[0].lower().replace("&", "and")

        item = (
            "\t<item>\n"
            f"\t\t<title><![CDATA[{title}]]></title>\n"
            "\t\t<dc:creator><![CDATA[admin]]></dc:creator>\n"
            f"\t\t<content:encoded><![CDATA[{body}]]></content:encoded>\n"
            "\t\t<excerpt:encoded><![CDATA[]]></excerpt:encoded>\n"
            f"\t\t<wp:post_id>{9000 + i}</wp:post_id>\n"
            f"\t\t<wp:post_date><![CDATA[{now}]]></wp:post_date>\n"
            f"\t\t<wp:post_date_gmt><![CDATA[{now}]]></wp:post_date_gmt>\n"
            "\t\t<wp:comment_status><![CDATA[closed]]></wp:comment_status>\n"
            "\t\t<wp:ping_status><![CDATA[closed]]></wp:ping_status>\n"
            f"\t\t<wp:post_name><![CDATA[{slug}]]></wp:post_name>\n"
            "\t\t<wp:status><![CDATA[publish]]></wp:status>\n"
            "\t\t<wp:post_parent>0</wp:post_parent>\n"
            f"\t\t<wp:menu_order>{i}</wp:menu_order>\n"
            "\t\t<wp:post_type><![CDATA[page]]></wp:post_type>\n"
            "\t\t<wp:post_password><![CDATA[]]></wp:post_password>\n"
            "\t\t<wp:is_sticky>0</wp:is_sticky>\n"
            + meta("_wp_page_template", template)
            + meta("_elementor_edit_mode", "builder")
            + meta("_elementor_template_type", "wp-page")
            + meta("_elementor_version", ELEMENTOR_VERSION)
            + meta("_elementor_data", data)
            + meta("site-sidebar-layout", sidebar)
            + meta("site-post-title", "disabled")
            + meta("ast-featured-img", "disabled")
            + meta("rank_math_title", seo_title)
            + meta("rank_math_description", seo_desc)
            + meta("rank_math_focus_keyword", focus)
            + "\t</item>\n"
        )
        items.append(item)

    wxr = (
        '<?xml version="1.0" encoding="UTF-8" ?>\n'
        '<rss version="2.0" xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wp="http://wordpress.org/export/1.2/">\n'
        "<channel>\n"
        "\t<title>SchnitzMenu</title>\n\t<link>https://schnitzmenu.com</link>\n"
        "\t<description>Schnitz Menu Australia - Prices, Calories &amp; Full Menu</description>\n"
        "\t<language>en-AU</language>\n\t<wp:wxr_version>1.2</wp:wxr_version>\n"
        "\t<wp:base_site_url>https://schnitzmenu.com</wp:base_site_url>\n"
        "\t<wp:base_blog_url>https://schnitzmenu.com</wp:base_blog_url>\n"
        "\t<wp:author><wp:author_id>1</wp:author_id><wp:author_login><![CDATA[admin]]></wp:author_login>"
        "<wp:author_email><![CDATA[]]></wp:author_email><wp:author_display_name><![CDATA[SchnitzMenu]]></wp:author_display_name>"
        "<wp:author_first_name><![CDATA[]]></wp:author_first_name><wp:author_last_name><![CDATA[]]></wp:author_last_name></wp:author>\n"
        + "".join(items)
        + "</channel>\n</rss>\n"
    )
    (ROOT / "import" / "schnitzmenu-pages.xml").write_text(wxr, encoding="utf-8")

    # Theme zip (folder name inside the zip must match the theme slug).
    with zipfile.ZipFile(ROOT / "dist" / "astra-child-schnitzmenu.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(THEME.rglob("*")):
            if f.is_file():
                z.write(f, f"astra-child-schnitzmenu/{f.relative_to(THEME)}")

    with zipfile.ZipFile(ROOT / "dist" / "elementor-templates.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted((ROOT / "elementor").glob("*.json")):
            z.write(f, f.name)

    print("Built", len(PAGES), "pages")
    for slug, n in report:
        print(f"  {slug:24} ~{n} words (+ tables/FAQ rendered by shortcodes)")


if __name__ == "__main__":
    main()
