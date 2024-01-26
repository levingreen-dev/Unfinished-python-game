import simpleaudio as sa

class maps:

    menuContent = {
        "m:menu": {
            "type": "1d",
            "items": [
                {
                    "id": "menu:main:inv",
                    "text": "Inventory",
                    "target": "menu:inv",
                },
                {
                    "text": "Quests",
                    "target": "menu:quests",
                },
                {
                    "text": "Save Game",
                    "target": "menu:save",
                },
                {
                    "text": "Load Game",
                    "target": "menu:load",
                },
                {
                    "text": "Exit Game",
                    "target": "quit:quit",
                },
            ],
        },
    }
    title = """
   _/      _/                      _/                        _/
_/_/_/_/  _/_/_/      _/_/        _/    _/_/_/    _/_/_/  _/_/_/_/
 _/      _/    _/  _/_/_/_/      _/  _/    _/  _/_/        _/
_/      _/    _/  _/            _/  _/    _/      _/_/    _/
 _/_/  _/    _/    _/_/_/      _/    _/_/_/  _/_/_/        _/_/



      _/_/_/
     _/    _/  _/  _/_/    _/_/_/    _/_/_/    _/_/    _/_/_/
    _/    _/  _/_/      _/    _/  _/    _/  _/    _/  _/    _/
   _/    _/  _/        _/    _/  _/    _/  _/    _/  _/    _/
  _/_/_/    _/          _/_/_/    _/_/_/    _/_/    _/    _/
                                     _/
                                 _/_/"""

    dieShape = {
        2: [
            "  ┌─┐  ",
            " /   \ ",
            "┌     ┐",
            "│     │",
            "└     ┘",
            " \   / ",
            "  └─┘  ",
        ],
        4: [
            "   ^   ",
            "  / \  ",
            " ┌   ┐ ",
            " ┘   └ ",
            "/     \\",
            "───────",
            "       ",
        ],
        6: [
            "┌─────┐",
            "│     │",
            "│     │",
            "│     │",
            "│     │",
            "│     │",
            "└─────┘",
        ],
        8: [
            "  ───  ",
            " /   \ ",
            "/     \\",
            "│     │",
            "\     /",
            " \   / ",
            "  ───  ",
        ],
        10: [
            "       ",
            " _-^-_ ",
            "<     >",
            " ┐   ┌ ",
            " └   ┘ ",
            "  \ /  ",
            "   v   ",
        ],
        12: [
            "   ^   ",
            " ┌   ┐ ",
            "┌     ┐",
            "\     /",
            " ┐   ┌ ",
            " └   ┘ ",
            "  ───  ",
        ],
        20: [
            "   ^  ",
            " ┌┘ └┐ ",
            "│     │",
            "│     │",
            "│     │",
            " └┐ ┌┘ ",
            "   v   ",
        ],
        100: [
            "  %%%  ",
            " %   % ",
            "%     %",
            "%     %",
            "%     %",
            " %   % ",
            "  %%%  ",
        ],
    }

    double = {
        "tl": "╔",
        "tr": "╗",
        "br": "╝",
        "bl": "╚",
        "h": "═",
        "v": "║",
    }
    thin = {
        "tl": "┌",
        "tr": "┐",
        "br": "┘",
        "bl": "└",
        "h": "─",
        "v": "│",
    }

    @staticmethod
    def border(which, style="double"):
        if which is None:
            return ""
        else:
            return getattr(maps, style)[which]

class assets:
    sounds = {
        "vine_boom": sa.WaveObject.from_wave_file("./audio.wav"),
        "anette": sa.WaveObject.from_wave_file("./anette.wav"),
    }