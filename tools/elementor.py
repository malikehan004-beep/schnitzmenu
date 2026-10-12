"""Tiny helpers that build Elementor (container-based) element trees.

Every string is kept free of backslashes and double quotes so the JSON survives
the WordPress importer untouched (it strips slashes from post meta).
"""
import hashlib

BRAND = "#D4471A"
BRAND_DARK = "#A8360F"
TINT = "#FFF3EE"
NAVY = "#1A1A2E"
GREY = "#F9F9F9"

_counter = [0]


def uid(seed=""):
    _counter[0] += 1
    return hashlib.md5(f"{seed}{_counter[0]}".encode()).hexdigest()[:7]


def reset_ids(seed):
    _counter[0] = sum(seed.encode())


def _pad(t, r, b, l):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": False}


def container(children, *, classes="", bg=None, pad=(40, 30, 40, 30), direction="column",
              element_id="", min_height=None, inner=False, width=None, gap=None, full=False, align=None):
    s = {
        "content_width": "full" if (full or inner) else "boxed",
        "flex_direction": direction,
        "padding": _pad(*pad),
        "padding_mobile": _pad(min(pad[0], 28), 16, min(pad[2], 28), 16),
    }
    if not inner:
        s["boxed_width"] = {"unit": "px", "size": 1200, "sizes": []}
    if direction == "row":
        s["flex_wrap"] = "wrap"
        s["flex_direction_mobile"] = "column"
    if gap is not None:
        s["flex_gap"] = {"unit": "px", "size": gap, "column": str(gap), "row": str(gap), "isLinked": True}
    if align:
        s["flex_align_items"] = align
    if classes:
        s["css_classes"] = classes
    if bg:
        s["background_background"] = "classic"
        s["background_color"] = bg
    if element_id:
        s["_element_id"] = element_id
    if min_height:
        s["min_height"] = {"unit": "px", "size": min_height, "sizes": []}
        s["flex_justify_content"] = "center"
    if width:
        s["width"] = {"unit": "%", "size": width, "sizes": []}
        s["width_mobile"] = {"unit": "%", "size": 100, "sizes": []}
    return {"id": uid("c"), "elType": "container", "settings": s, "elements": children, "isInner": inner}


def widget(kind, settings, classes=""):
    if classes:
        settings["_css_classes"] = classes
    return {"id": uid("w"), "elType": "widget", "widgetType": kind, "settings": settings, "elements": []}


def heading(text, tag="h2", align=None, color=None, size=None, classes=""):
    s = {"title": text, "header_size": tag}
    if align:
        s["align"] = align
    if color:
        s["title_color"] = color
    if size:
        s["typography_typography"] = "custom"
        s["typography_font_family"] = "Montserrat"
        s["typography_font_weight"] = "700"
        s["typography_font_size"] = {"unit": "px", "size": size, "sizes": []}
        s["typography_font_size_mobile"] = {"unit": "px", "size": max(22, int(size * 0.68)), "sizes": []}
    return widget("heading", s, classes)


def text(html, align=None, color=None, size=None, classes=""):
    s = {"editor": html}
    if align:
        s["align"] = align
    if color:
        s["text_color"] = color
    if size:
        s["typography_typography"] = "custom"
        s["typography_font_size"] = {"unit": "px", "size": size, "sizes": []}
    return widget("text-editor", s, classes)


def button(label, url, align=None, bg=BRAND, fg="#FFFFFF", classes=""):
    s = {
        "text": label,
        "link": {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""},
        "background_color": bg,
        "button_text_color": fg,
        "border_radius": {"unit": "px", "top": "6", "right": "6", "bottom": "6", "left": "6", "isLinked": True},
        "typography_typography": "custom",
        "typography_font_family": "Montserrat",
        "typography_font_weight": "700",
    }
    if align:
        s["align"] = align
    return widget("button", s, classes)


def shortcode(code):
    return widget("shortcode", {"shortcode": code})


def html(code, classes=""):
    return widget("html", {"html": code}, classes)


def walk(elements):
    for el in elements:
        yield el
        yield from walk(el.get("elements", []))
