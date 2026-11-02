# AlikeZelda

A retro top-down action game built with Python and Pygame for Hack Club Terra's antique theme. Explore the village, forest, and ruins, claim all three cursed chest rewards, then escape through the ruins gate.

## Features

- One connected 64 × 40 map with 12 squid enemies, four ordinary chests, and three cursed chests.
- Cursed chest duels against a reflection that repeats your attacks and spells after a delay.
- Collectible weapons with common, rare, and epic rarities. Stronger duplicates replace weaker ones.
- Healing and directional flame spells, energy recovery, and XP upgrades for health, energy, attack, magic, and speed.
- A paused world map that reveals terrain as you explore and marks discovered chests and the exit.
- Three treasure clues leading to buried caches with rare or epic weapons and 100 XP each.
- A title screen, interaction prompts, a cursed chest objective, and death/victory screens with restart controls.

Saving is still in progress. The code can write a JSON snapshot, but automatic saving and restoring progress are not connected to gameplay yet. Closing or restarting the game resets the run.

## Run

Install Python 3.14, download or clone the repository, and open a terminal in the project folder. Create and activate a virtual environment, then run:

```sh
python -m pip install -r requirements.txt
python code/main.py
```

Run from the project folder so the game can find its graphics and maps. Tested with Python 3.14 and pygame-ce 2.5.8. The package is called `pygame-ce`, but the code imports it as `pygame`.

## Controls

| Key | Action |
| --- | --- |
| Enter | Start from the title screen |
| Arrow keys | Move; select a stat while the upgrade screen is open |
| Space | Attack; purchase the selected upgrade while the upgrade screen is open |
| Q | Switch between collected weapons |
| E | Switch spell |
| Left Ctrl | Cast the selected spell |
| F | Interact with chests, clues, buried treasure, and the exit |
| Tab | Open/close the world map and pause/resume |
| M | Open/close the upgrade screen and pause/resume |
| R | Start a fresh run after dying or escaping |

## Credits

- Weapon and enemy artwork, spell icons, and spell/combat animations: Pixel-boy and AAA — [Ninja Adventure Asset Pack](https://pixel-boy.itch.io/ninja-adventure-asset-pack).
- Joystix font: Raymond Larabie / Typodermic Fonts — [Joystix](https://typodermicfonts.com/between-the-lines/stories/joystix/).
