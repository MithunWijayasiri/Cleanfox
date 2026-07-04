# CLEANFOX Firefox Config

[![Sync with Betterfox](https://github.com/MithunWijayasiri/Cleanfox/actions/workflows/sync.yml/badge.svg)](https://github.com/MithunWijayasiri/Cleanfox/actions/workflows/sync.yml)
[![License: MIT](https://img.shields.io/github/license/MithunWijayasiri/Cleanfox)](LICENSE)
[![Firefox](https://img.shields.io/badge/Firefox-user.js-orange?logo=firefoxbrowser&logoColor=white)](https://www.mozilla.org/firefox/)
[![Betterfox](https://img.shields.io/badge/Based_on-Betterfox-blue)](https://github.com/yokoffing/Betterfox)

CLEANFOX is a Firefox `user.js` configuration built on top of [Betterfox](https://github.com/yokoffing/Betterfox). It keeps the Betterfox performance and privacy baseline, relaxes a few defaults for everyday browsing, and adds a small set of personal UI preferences.

Tested with Firefox, Firefox Nightly, and Firefox ESR.

## Table of Contents

- [Install](#install)
- [Update](#update)
- [Sync With Betterfox](#sync-with-betterfox)
- [Betterfox Differences](#betterfox-differences)
- [Optional Preferences](#optional-preferences)
- [Recommended Add-ons](#recommended-add-ons)
- [Resources](#resources)
- [Credits](#credits)

## Install

1. Install [Firefox](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release), if needed.
2. Download [`user.js`](https://github.com/MithunWijayasiri/Cleanfox/raw/main/user.js).
3. Open Firefox and go to `about:profiles`.
4. Find the profile you want to use.
5. Click **Open Folder** under **Root Directory**.
6. Place `user.js` in that folder.
7. Restart Firefox.

You can also download the full repository as a [ZIP archive](https://github.com/MithunWijayasiri/Cleanfox/archive/refs/heads/main.zip).

## Update

Replace the existing profile `user.js` with the latest version from this repository, then restart Firefox.

## Sync With Betterfox

`user.js` is generated from upstream Betterfox by [`build.py`](build.py). The script fetches Betterfox, applies the CLEANFOX changes, writes `user.js`, and stores the upstream snapshot in [`upstream/betterfox.user.js`](upstream/betterfox.user.js).

A monthly GitHub Action runs the sync automatically on the first day of each month. It can also be triggered manually from the **Actions** tab.

Run a local sync:

```bash
python build.py
```

Run a local sync from a downloaded Betterfox file:

```bash
python build.py --upstream path/to/user.js
```

## Betterfox Differences

CLEANFOX keeps Betterfox as the base config, then applies these changes.

### Changed Defaults

| Preference | Betterfox | CLEANFOX | Reason |
| --- | --- | --- | --- |
| `browser.contentblocking.category` | `strict` | `standard` | Avoids breakage with some logins, embeds, and comment widgets. |
| `browser.cache.disk.enable` | `false` | `true` | Keeps disk cache for faster repeat visits and lower bandwidth use. |
| `browser.search.suggest.enabled` | `false` | `true` | Keeps address-bar search suggestions and autocomplete. |
| `browser.download.manager.addToRecentDocs` | `false` | removed | Allows downloads to appear in the OS recent-files list. |
| `browser.ai.*` / `browser.ml.*` | disabled | removed | Leaves Firefox AI features at their browser defaults. |

### Added Preferences

| Preference | Description |
| --- | --- |
| `ui.key.menuAccessKeyFocuses` | Disables the menu opening when pressing `Alt`. |
| `browser.tabs.warnOnClose` | Disables the confirmation prompt when closing a window with multiple tabs. |
| `browser.urlbar.openViewOnFocus` | Disables the address bar pop-out on focus. |
| `browser.tabs.hoverPreview.enabled` | Disables tab previews on hover. |
| `layout.word_select.eat_space_to_next_word` | Prevents double-click word selection from including the trailing space. |

## Optional Preferences

The bottom of [`user.js`](user.js) includes commented preferences for stricter behavior. Uncomment only the options you want.

Available optional blocks:

- Disable Firefox AI features.
- Stop adding downloads to the OS recent-files list.
- Disable DRM content.
- Disable Firefox Sync-related features.
- Disable OS geolocation service integration.

## Recommended Add-ons

- [uBlock Origin](https://addons.mozilla.org/blog/ublock-origin-everything-you-need-to-know-about-the-ad-blocker/) - ad blocker. Optional: [recommended filters](https://t.me/jCloud1/470).
- [Enhancer for YouTube](https://addons.mozilla.org/en-US/firefox/addon/enhancer-for-youtube/) - extra YouTube controls and features.
- [Privacy Badger](https://addons.mozilla.org/en-US/firefox/addon/privacy-badger17/) - tracker blocking based on observed behavior.
- [Sessionic](https://addons.mozilla.org/en-US/firefox/addon/sessionic/) - session save, manage, and restore tools.
- [Duplicate Tab Shortcut](https://addons.mozilla.org/en-US/firefox/addon/duplicate-tab-shortcut/) - `Alt` + `Shift` + `D` shortcut for duplicating the current tab.

## Resources

- [Personal Data Leak Check](https://personaldata.info/#about)
- [Firefox Hardening Guide](https://brainfucksec.github.io/firefox-hardening-guide)
- [ArchWiki: Firefox Privacy Configuration](https://wiki.archlinux.org/title/Firefox/Privacy#Configuration)

## Credits

- [Betterfox](https://github.com/yokoffing/Betterfox) for the base Firefox configuration.

## License

Released under the [MIT License](LICENSE).

<div align="center">
  <a href="https://www.websitecounterfree.com"><img src="https://www.websitecounterfree.com/c.php?d=9&id=48832&s=3" border="0" alt="Free Website Counter"></a><br>
  since 05 Feb 2024
</div>
