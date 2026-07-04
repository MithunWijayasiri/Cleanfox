# CLEANFOX Firefox Config
user.js for clean, fast, private Firefox.
- Tested this user.js on Firefox, Firefox Nightly, Firefox ESR.

## Getting started
*If you don't have firefox already: [Get Firefox](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release)*

1) Download the user.js file [here](https://github.com/MithunWijayasiri/Cleanfox/raw/main/user.js) (Or download source > [Click Here](https://github.com/MithunWijayasiri/Cleanfox/archive/refs/heads/main.zip))
2) Open Firefox. In the URL bar, type `about:profiles` and press **Enter**.
3) For the profile you want to use (or use default), click **Open Folder** in the **Root Directory** section.
4) Move the `user.js` file into the folder.
5) Done.

## Difference with Betterfox Config

CLEANFOX takes Betterfox as-is, relaxes a few of its more aggressive defaults, and appends my own preferences. Everything below is re-applied automatically by `build.py` on each sync.

### Changes to Betterfox defaults

| Code | Betterfox | CLEANFOX | Why |
| :--- | :---: | :---: | :--- |
| `browser.contentblocking.category` | `strict` | `standard` | Strict tracking protection breaks some logins, embeds and comment widgets |
| `browser.cache.disk.enable` | `false` | `true` | Keep the disk cache — avoids re-downloading assets on every restart (faster, less bandwidth) |
| `browser.search.suggest.enabled` | `false` | `true` | Keep address-bar search suggestions / autocomplete |
| `browser.download.manager.addToRecentDocs` | `false` | removed | Downloads show in the OS recent-files list; uncomment the block in the CLEANFOX footer to block it |
| `browser.ai.*` / `browser.ml.*` | disabled | enabled | Firefox AI features left on by default; uncomment the AI block in the CLEANFOX footer to disable them |

### Personal preferences added

| Code | Description |
| :--- | :--- |
| `ui.key.menuAccessKeyFocuses` | Disable menu popping up when pressing the ALT key |
| `browser.tabs.warnOnClose` | Disable confirmation prompt when closing a window with multiple tabs |
| `browser.urlbar.openViewOnFocus` | Disable address bar popping out |
| `browser.tabs.hoverPreview.enabled` | Disable tab previews when hovering over them |
| `layout.word_select.eat_space_to_next_word` | Double-click word selection no longer includes the trailing space |

## Staying in sync with Betterfox

`user.js` is generated from upstream Betterfox by `build.py`, which re-applies the CLEANFOX changes on top. A monthly GitHub Action ([`.github/workflows/sync.yml`](.github/workflows/sync.yml)) rebuilds it automatically; it can also be run on demand from the **Actions** tab, or locally with `python build.py`. Customizations live as constants at the top of `build.py`.

## Note
> [!IMPORTANT]
> There are a few extra things available at the bottom of the user.js file. Enable them if you need.

## Recommended Addons
1) [uBlock Origin](https://addons.mozilla.org/blog/ublock-origin-everything-you-need-to-know-about-the-ad-blocker/) - Adblocker | [Recommended filters](https://t.me/jCloud1/470)
2) [Enhancer for YouTube™](https://addons.mozilla.org/en-US/firefox/addon/enhancer-for-youtube/) - Additional features for YouTube
3) [Privacy Badger](https://addons.mozilla.org/en-US/firefox/addon/privacy-badger17/) - Automatically learns to block invisible trackers
4) [Sessionic](https://addons.mozilla.org/en-US/firefox/addon/sessionic/) - Save, manage and restore sessions
4) [Duplicate Tab Shortcut](https://addons.mozilla.org/en-US/firefox/addon/duplicate-tab-shortcut/) - Press Alt+Shift+D to duplicate the current tab

## Additional Readings
* [Check what information your device exposes to the web](https://personaldata.info/#about)
* [Firefox Hardening Guide](https://brainfucksec.github.io/firefox-hardening-guide)
* [archlinux article about Firefox configuration](https://wiki.archlinux.org/title/Firefox/Privacy#Configuration)

## Credit
* Many thanks to the [Betterfox](https://github.com/yokoffing/Betterfox) team for the base config.

<div align='center'>
  <a href='https://www.websitecounterfree.com'><img src='https://www.websitecounterfree.com/c.php?d=9&id=48832&s=3' border='0' alt='Free Website Counter'></a><br/>
since 05 Feb 2024</div>
