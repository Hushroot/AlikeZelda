# AlikeZelda

A work-in-progress retro top-down game built with Python and Pygame for Hack Club Terra's antique theme.

## Current features

- Four-direction movement and walking animations
- Rock collisions and a camera that follows the player
- CSV-based map and sprites drawn in vertical order
- Five selectable weapons with temporary attack sprites
- Health, energy, selected-weapon, and experience displays

This is an early prototype. The health, energy, and experience values are currently demo values. Enemies, damage, and magic effects are still to come.

## Run

Create and activate a Python virtual environment, then run these commands from the project folder:

```sh
python -m pip install -r requirements.txt
python code/main.py
```

Tested with Python 3.14 and pygame-ce 2.5.8. The package is called `pygame-ce`, but the code imports it as `pygame`.

## Controls

| Key | Action |
| --- | --- |
| Arrow keys | Move |
| Space | Attack |
| Q | Switch weapon |

## Credits

- Weapon artwork: Pixel-boy and AAA — [Ninja Adventure Asset Pack](https://pixel-boy.itch.io/ninja-adventure-asset-pack).
- Joystix font: Raymond Larabie / Typodermic Fonts — [Joystix](https://typodermicfonts.com/between-the-lines/stories/joystix/).
