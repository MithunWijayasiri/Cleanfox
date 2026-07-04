#!/usr/bin/env python3
"""Build CLEANFOX user.js by applying the recipe to upstream Betterfox user.js.

Fetches upstream, applies pref-keyed customizations, writes user.js and a
committed snapshot of upstream (so each sync's git diff shows Betterfox changes).
Stdlib only. Run: python build.py [--upstream PATH]
"""
import argparse
import re
import sys
import urllib.request
from pathlib import Path

UPSTREAM_URL = "https://raw.githubusercontent.com/yokoffing/Betterfox/main/user.js"
ROOT = Path(__file__).resolve().parent

# --- RECIPE ---------------------------------------------------------------
CLEANFOX_VERSION = "2.0"  # bump manually on release
HEADER_TITLE = "CLEANFOX"
HEADER_MOTTO = '"MithunWijayasiri"'
HEADER_URL = "https://github.com/MithunWijayasiri/Cleanfox"

# Per-section overlays applied to upstream (keyed by pref name).
OVERLAYS = {
    "FASTFOX": {"set": {}, "remove": [], "disable": [], "add": []},
    "SECUREFOX": {
        "set": {
            # Relax Betterfox defaults that hurt everyday UX.
            "browser.contentblocking.category": '"standard"',  # strict breaks some sites
            "browser.cache.disk.enable": "true",               # keep disk cache (faster repeat visits)
            "browser.search.suggest.enabled": "true",          # keep address-bar suggestions
        },
        "remove": [],
        "disable": [],
        "add": [],
    },
    "PESKYFOX": {
        "set": {},
        # Moved to the footer TRY YOURSELF block (commented) — off by default.
        "remove": [
            "browser.ai.control.default",
            "browser.ml.enable",
            "browser.ml.chat.enabled",
            "browser.ml.chat.menu",
            "browser.tabs.groups.smart.enabled",
            "browser.ml.linkPreview.enabled",
            "browser.download.manager.addToRecentDocs",
        ],
        "disable": [],
        "add": [
            ('layout.word_select.eat_space_to_next_word', 'false'),
        ],
    },
}

# Frozen CLEANFOX footer body (between the SECTION and END banners).
# Replaces upstream SMOOTHFOX + MY OVERRIDES placeholders (comments only, no prefs).
FOOTER_BODY = '''
/** PERSONAL PREFERENCES ***/
user_pref("ui.key.menuAccessKeyFocuses", false);

// Ask for confirmation when closing a window with multiple tabs
user_pref("browser.tabs.warnOnClose", false);

// Disable address bar popping out
user_pref("browser.urlbar.openViewOnFocus", false);

// Disable tab previews when hovering over them
user_pref("browser.tabs.hoverPreview.enabled", false);

/** TRY YOURSELF ***/
// PREF: disable Firefox AI features
// user_pref("browser.ai.control.default", "blocked");
// user_pref("browser.ml.enable", false);
// user_pref("browser.ml.chat.enabled", false);
// user_pref("browser.ml.chat.menu", false);
// user_pref("browser.tabs.groups.smart.enabled", false);
// user_pref("browser.ml.linkPreview.enabled", false);

// PREF: don't add downloads to the OS recent-files list
// user_pref("browser.download.manager.addToRecentDocs", false);

// PREF: disable all DRM content
// user_pref("media.eme.enabled", false);

// PREF: disable Firefox Sync
// user_pref("identity.fxaccounts.enabled", false);
// user_pref("dom.push.enabled", false);
// user_pref("dom.push.connection.enabled", false);
// user_pref("browser.tabs.firefox-view", false);

// PREF: disable using the OS's geolocation service
// user_pref("geo.provider.ms-windows-location", false); // [WINDOWS]
// user_pref("geo.provider.use_corelocation", false); // [MAC]
// user_pref("geo.provider.use_gpsd", false); // [LINUX] broken on Linux?
// user_pref("geo.provider.use_geoclue", false); // [FF102+] [LINUX]'''

# --- PARSING --------------------------------------------------------------
PREF_RE = re.compile(r'^(\s*)user_pref\("([^"]+)",\s*(.*?)\);(.*)$')
SUBHEADER_RE = re.compile(r'^\s*/\*\*.*\*\*\*/\s*$')  # /** NAME ***/ subsection header


def drop_empty_subsections(lines):
    """Drop a /** NAME ***/ header (and its trailing blanks) if the overlay
    removed every pref under it."""
    out = []
    i = 0
    while i < len(lines):
        if SUBHEADER_RE.match(lines[i]):
            j = i + 1
            while j < len(lines) and not SUBHEADER_RE.match(lines[j]):
                j += 1
            if not any(lines[k].strip() for k in range(i + 1, j)):
                i = j
                continue
        out.append(lines[i])
        i += 1
    return out


def marker_index(lines, name):
    for i, l in enumerate(lines):
        if name in l and l.lstrip().startswith("*"):
            return i
    raise SystemExit(f"marker not found: {name}")


def section_body(lines, start, end):
    """Lines between the banner of `start` marker and the banner of `end` marker.

    Banners are 3 lines (top rule / middle / bottom rule)."""
    s = marker_index(lines, start)
    e = marker_index(lines, end)
    return lines[s + 2:e - 1]


def apply_overlay(body, ov):
    out = []
    for line in body:
        m = PREF_RE.match(line)
        if not m:
            out.append(line)
            continue
        indent, key, val, trail = m.group(1), m.group(2), m.group(3), m.group(4)
        if key in ov["remove"]:
            continue
        if key in ov["disable"]:
            out.append(f'{indent}// user_pref("{key}", {val});{trail} [CLEANFOX]')
            continue
        if key in ov["set"]:
            out.append(f'{indent}user_pref("{key}", {ov["set"][key]});{trail}')
            continue
        out.append(line)
    out = drop_empty_subsections(out)
    while out and not out[-1].strip():
        out.pop()
    for key, val in ov["add"]:
        out.append(f'user_pref("{key}", {val});')
    return out


# --- BANNERS --------------------------------------------------------------
def make_banner(width, *content):
    top = "/" + "*" * (width - 1)
    bot = "*" * (width - 1) + "/"
    mid = [f" * {t}".ljust(width - 1) + "*" for t in content]
    return [top, *mid, bot]


def build(upstream_text):
    lines = upstream_text.splitlines()

    bx = next((i for i, l in enumerate(lines) if l.lstrip().startswith("* Betterfox")), None)
    if bx is None:
        raise SystemExit("marker not found: * Betterfox header")
    width = len(lines[bx - 1])
    version_m = re.search(r"version:\s*(\d+)", upstream_text)
    upstream_version = version_m.group(1) if version_m else "?"

    preamble = lines[:bx - 1]

    header = make_banner(
        width,
        HEADER_TITLE,
        HEADER_MOTTO,
        f"version: {CLEANFOX_VERSION} (synced with Betterfox v{upstream_version})",
        f"url: {HEADER_URL}",
    )

    fastfox = make_banner(width, "SECTION: FASTFOX") + apply_overlay(
        section_body(lines, "SECTION: FASTFOX", "SECTION: SECUREFOX"), OVERLAYS["FASTFOX"]
    )
    securefox = make_banner(width, "SECTION: SECUREFOX") + apply_overlay(
        section_body(lines, "SECTION: SECUREFOX", "SECTION: PESKYFOX"), OVERLAYS["SECUREFOX"]
    )
    peskyfox = make_banner(width, "SECTION: PESKYFOX") + apply_overlay(
        section_body(lines, "SECTION: PESKYFOX", "SECTION: SMOOTHFOX"), OVERLAYS["PESKYFOX"]
    )
    footer = (
        make_banner(width, "SECTION: CLEANFOX")
        + FOOTER_BODY.splitlines()
        + [""]
        + make_banner(width, "END: CLEANFOX")
    )

    blocks = [preamble, header, fastfox, securefox, peskyfox, footer]
    text = "\n\n".join("\n".join(b).strip("\n") for b in blocks)
    return text.rstrip("\n") + "\n", upstream_version


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", help="path to a local upstream user.js (skip fetch)")
    args = ap.parse_args()

    if args.upstream:
        upstream_text = Path(args.upstream).read_text(encoding="utf-8")
    else:
        with urllib.request.urlopen(UPSTREAM_URL, timeout=30) as r:
            upstream_text = r.read().decode("utf-8")

    out, version = build(upstream_text)
    (ROOT / "user.js").write_text(out, encoding="utf-8", newline="\n")
    snap = ROOT / "upstream" / "betterfox.user.js"
    snap.parent.mkdir(exist_ok=True)
    snap.write_text(upstream_text, encoding="utf-8", newline="\n")
    print(f"built user.js from Betterfox v{version}")


if __name__ == "__main__":
    main()
