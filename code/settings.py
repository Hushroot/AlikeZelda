WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

WORLD_MAP = [
    'xxxxxxxxxx',
    'xp       x',
    'x  xx    x',
    'x        x',
    'x      x x',
    'xxxxxxxxxx',
]

weapon_data = {
    'sword': {
        'cooldown': 100, 
        'damage': 15, 
        'graphic': 'graphics/weapons/sword/full.png'
        },
    'lance': {
        'cooldown': 400, 
        'damage': 30, 
        'graphic': 'graphics/weapons/lance/full.png'
        },
    'axe': {
        'cooldown': 300, 
        'damage': 20, 
        'graphic': 'graphics/weapons/axe/full.png'
        },
    'rapier': {
        'cooldown': 50, 
        'damage': 8, 
        'graphic': 'graphics/weapons/rapier/full.png'
        },
    'sai': {
        'cooldown': 80, 
        'damage': 10, 
        'graphic': 'graphics/weapons/sai/full.png'
        }
}
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140

UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
ITEM_BOX_SIZE = 80
UI_BORDER_COLOR_ACTIVE = 'gold'
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
TEXT_COLOR = '#EEEEEE'

magic_data = {
    'flame': {
        'strength': 5,
        'cost': 20,
        'graphic': 'graphics/particles/flame/fire.png'
    },
    'heal': {
        'strength': 20,
        'cost': 10,
        'graphic': 'graphics/particles/heal/heal.png'
    }
}

monster_data = {
    'squid': {
        'health': 100,
        'exp': 100,
        'damage': 20,
        'attack_type': 'slash',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 80,
        'notice_radius': 360
    }
}

TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

rarity_data = {
    'common': {'weight': 70, 'multiplier': 1, 'color': '#b8b8b8'},
    'rare': {'weight': 25, 'multiplier': 1.5, 'color': '#5599ff'},
    'epic': {'weight': 5, 'multiplier': 2, 'color': '#bb66ff'}
}