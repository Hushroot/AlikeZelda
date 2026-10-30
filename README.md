# AlikeZelda

A work-in-progress retro top-down game built with Python and Pygame for Hack Club Terra's antique theme.

## Current features

- Four-direction movement and walking animations
- Rock collisions and a camera that follows the player
- CSV-based map and sprites drawn in vertical order
- Five selectable weapons with temporary attack sprites
- Health, energy, selected-weapon, and experience displays
- Animated squid enemy that notices, chases, and attacks the player
- Weapon damage, enemy defeat, and brief protection after taking a hit
- Flame/heal selection with an on-screen icon

This is an early prototype. Player health now responds to enemy attacks; energy and experience still use demo values. Spell effects and energy spending are still to come. The spell test currently prints the selected spell's details in the terminal.

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
| E | Switch spell |
| Left Ctrl | Spell test (terminal output) |

## Credits

- Weapon and enemy artwork, and spell icons: Pixel-boy and AAA — [Ninja Adventure Asset Pack](https://pixel-boy.itch.io/ninja-adventure-asset-pack).
- Joystix font: Raymond Larabie / Typodermic Fonts — [Joystix](https://typodermicfonts.com/between-the-lines/stories/joystix/).
