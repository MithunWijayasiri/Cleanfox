# Betterfox vs CLEANFOX

Changes CLEANFOX applies to upstream [Betterfox `user.js`](https://github.com/yokoffing/Betterfox/blob/main/user.js).
Applied by `build.py` on every sync — keyed by pref name, not line number.

Base: latest upstream Betterfox `main`. Synced version is recorded in the `user.js`
header (`synced with Betterfox vNNN`), auto-filled per build — not pinned here.

## Header

- Betterfox banner → CLEANFOX banner.
- `synced with Betterfox vNNN` auto-filled from fetched upstream version.
- CLEANFOX release version manual (`CLEANFOX_VERSION` in `build.py`).
- Added top comment: `// ... search for the [#$] keyword.`

| Field | Value | Constant |
|---|---|---|
| title | `CLEANFOX` | `HEADER_TITLE` |
| motto | `"MithunWijayasiri"` | `HEADER_MOTTO` |
| url | `https://github.com/MithunWijayasiri/Cleanfox` | `HEADER_URL` |

## FASTFOX — frozen

Upstream FASTFOX (GENERAL / GFX / JS / MEDIA / IMAGE / NETWORKING) discarded, replaced with:

| Pref | Value | Note |
|---|---|---|
| `gfx.canvas.accelerated.cache-size` | `256` | upstream ships `512` |
| `gfx.webrender.layer-compositor` | `true` | added |

New upstream FASTFOX prefs are **not** picked up. Add to `FASTFOX_BODY` to adopt.

## SECUREFOX — passthrough

Taken from upstream as-is. New Betterfox security prefs flow in automatically.

## PESKYFOX — passthrough + overlay

| Pref | Change |
|---|---|
| `browser.download.manager.addToRecentDocs` | commented out, tagged `[CLEANFOX]` |
| `browser.menu.showViewImageInfo` = `true` | added |
| `layout.word_select.eat_space_to_next_word` = `false` | added |

## Footer — frozen

Upstream SMOOTHFOX + MY-OVERRIDES placeholders replaced with `SECTION: CLEANFOX`.

Personal prefs (active):

| Pref | Value |
|---|---|
| `ui.key.menuAccessKeyFocuses` | `false` |
| `browser.tabs.warnOnClose` | `false` |
| `browser.urlbar.openViewOnFocus` | `false` |
| `browser.tabs.hoverPreview.enabled` | `false` |

"Try Yourself" (commented, opt-in): DRM (`media.eme.enabled`), Firefox Sync
(`identity.fxaccounts.enabled` + push), OS geolocation providers.

## Dropped by upstream

`browser.privatebrowsing.resetPBM.enabled` — present in v148, removed by Betterfox in v152.
CLEANFOX tracks upstream (SECUREFOX passthrough), so it's gone. Re-add via SECUREFOX `set` overlay to keep.

## Editing the recipe

All changes above live as constants at the top of `build.py`:
`FASTFOX_BODY`, `OVERLAYS` (`set` / `remove` / `disable` / `add` per section), `FOOTER_BODY`, header fields.
