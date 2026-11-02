# AlikeZelda browser build

This branch contains the browser demo built from source commit `3a5dc6c7ffbe75222be663c7044e961c5d9d50f0` on `main`.

Open the published GitHub Pages site in a desktop browser, click the game once after loading, then press Enter. Arrow keys move, Space attacks, F interacts, Tab opens the map, and M opens upgrades. Progress resets when the page is reloaded.

The build uses Pygbag 0.9.3. Its Python 3.12 runtime and pygame-ce load from the official pygame-web CDN. `source.tar.gz` is the game archive used on GitHub Pages; `source.apk` supports the alternate itch.io loader. The main loop uses asyncio so the browser can render each frame. Environment and player images are packaged at the exact sizes already rendered by the game; pixel comparisons passed against the desktop scaling results.

The desktop game source is on the `main` branch. Saving is still in progress there; automatic saving and restoring progress are not connected yet.

## Credits

- Weapon and enemy artwork, spell icons, and spell/combat animations: Pixel-boy and AAA — [Ninja Adventure Asset Pack](https://pixel-boy.itch.io/ninja-adventure-asset-pack).
- Joystix font: Raymond Larabie / Typodermic Fonts — [Joystix](https://typodermicfonts.com/between-the-lines/stories/joystix/).
