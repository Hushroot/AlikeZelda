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
- Flashing hit feedback, enemy knockback, and slash/death effects
- Healing and directional flame spells with animated effects and energy costs
- Gradual energy recovery
- 100 XP earned for defeating the squid
- A pause screen with five upgrade panels showing stats, limits, and XP costs

This is an early prototype. The upgrade panels are currently a display; keyboard selection and purchasing are the next step. Progress resets when the game restarts.

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
| Left Ctrl | Cast selected spell |
| M | Open/close the upgrade screen and pause/resume |

## Credits

- Weapon and enemy artwork, spell icons, and spell/combat animations: Pixel-boy and AAA — [Ninja Adventure Asset Pack](https://pixel-boy.itch.io/ninja-adventure-asset-pack).
- Joystix font: Raymond Larabie / Typodermic Fonts — [Joystix](https://typodermicfonts.com/between-the-lines/stories/joystix/).
