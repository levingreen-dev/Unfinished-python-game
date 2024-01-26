#!/usr/bin/env python3

import tcod
import random
import time
import math
import threading
import re

import json
from collections import OrderedDict

import simpleaudio as sa
import textwrap

from actions import *
from maps import maps
from input_handlers import EventHandler

from character import character

WIDTH, HEIGHT = 960, 400

FLAGS = tcod.context.SDL_WINDOW_RESIZABLE=False

# colors (gruvbox)

#WHITE       = (235, 219, 178)
#BLACK       = ( 40,  40,  40)
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
RED         = (204,  36,  29)
GREEN       = (152, 151,  26)
YELLOW      = (215, 153,  33)
BLUE        = ( 69, 133, 136)
PURPLE      = (177,  98, 134)
AQUA        = (104, 157, 106)
ORANGE      = (214,  93,  14)

RED_L       = (251,  73,  52)
GREEN_L     = (184, 187,  38)
YELLOW_L    = (250, 189,  47)
BLUE_L      = (131, 165, 152)
PURPLE_L    = (211, 134, 155)
AQUA_L      = (142, 192, 124)
ORANGE_L    = (254, 128,  25)

def main():
    screen_w = 120
    screen_h = 50

    tileset = tcod.tileset.load_tilesheet(
        "CGA8x8thick.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    commands = {
        "m:quests": showQuestList()
    }

    state = 0 # 0 = title, 1 = menu, 2 = main, 3 = other
    other = ["mainGUI"]

    inp = ""
    inpFocus = False
    command = ""
    promptWaiting = False
    reading = ""

    player = character(30, 20, "none", 5, 20)
    titlescreen = False # is active, is waiting
    activeQuest = ""
    with open("./story/index.json", "r") as index:
        questIndex = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(index.read())
    questData = {}
    questProgress = ["", 0] #[["<sect name>", <sect index>] <content index>]
    questSectLen = 0 # amount of dialog in a section in a quest
    questLoading = [False, False] # reload quests when open quests menu
    questNext = False # whether or not to show next dialog in quest
    isFighting = False
    turn = "player"

    roll = 0
    rolled = False
    dieSize = 0
    rolling = False
    rollCount = 0
    rollTime = 0
    rollWait = False

    wait = False

    menu = ""
    select = [0, 0]
    menuSelectable = False
    menuType = "1d"
    menuAction = ""
    menuWaiting = ""

    invMove = None

    dispwidth = 80
    dispheight = 30

    titlescreenFades = [1, 1, 1, 1, False, False]

    # load audio files

    bg_sound = None
    soundFiles = {
        "vine_boom": sa.WaveObject.from_wave_file("./audio.wav"),
        "anette": sa.WaveObject.from_wave_file("./anette.wav"),
    }

    global display_text
    display_text = []

    event_handler = EventHandler()

    with tcod.context.new(
        width=WIDTH,
        height=HEIGHT,
        tileset=tileset,
        title="𝐙𝐞𝐩𝐡𝐫𝐞𝐧 𝐭𝐡𝐞 𝐥𝐚𝐬𝐭 𝐝𝐫𝐚𝐠𝐨𝐧",
        vsync=True,
        sdl_window_flags=FLAGS,
    ) as context:
        while True:
            global console
            console = context.new_console(screen_w, screen_h, order="F")

            if re.search("^quit:", menu):
                raise SystemExit()

            if state == 0:
                if not bg_sound or not bg_sound.is_playing():
                    bg_sound = soundFiles["anette"].play()
                sect(0, 0, screen_w, screen_h)

                if titlescreenFades[4]:
                    if titlescreenFades[3] >= 128:
                        titlescreenFades[5] = False
                    if titlescreenFades[3] <= 92:
                        titlescreenFades[5] = True
                    if titlescreenFades[5]:
                        titlescreenFades[3] += 1
                    else:
                        titlescreenFades[3] -= 1
                elif titlescreenFades[0] < 128:
                    titlescreenFades[0] += 1
                elif titlescreenFades[1] < 128:
                    titlescreenFades[1] += 1
                elif titlescreenFades[2] < 128:
                    titlescreenFades[2] += 1
                elif titlescreenFades[3] < 128:
                    titlescreenFades[3] += 1
                else:
                    titlescreenFades[4] = True
                console.print(40, 39, "-- Made by dublUayaychtee and blainto --", fg=[titlescreenFades[0] * 2 - 1, titlescreenFades[0] * 2 - 1, titlescreenFades[0] * 2 - 1])
                console.print(52, 40, "-- zyphren --", fg=[titlescreenFades[1] * 2 - 1, titlescreenFades[1] * 2 - 1, titlescreenFades[1] * 2 - 1])
                console.print(26, 10, maps.title, fg=[titlescreenFades[2] * 2 - 1, titlescreenFades[2] * 2 - 1, titlescreenFades[2] * 2 - 1])
                if titlescreenFades[3] > 64:
                    console.print(48, 35, "Press Enter to Continue", fg=[(titlescreenFades[3] - 64) * 4 - 1, (titlescreenFades[3] - 64) * 4 - 1, (titlescreenFades[3] - 64) * 4 - 1])

            elif state == 1:
                # blank ui elements
                console.print(1, 1, "menu not made yet if you see this something is b0rked")
                state = 2
                pass

            elif state == 2:

                if command == "testitem":
                    if not player.invCheckEmpty():
                        disp("No Room!")
                    else:
                        player.invAddItem({"name": "testItem"})
                    command = ""

                # display box
                sect(0, 0, 81, 31, right=False, bottom=False)
                
                # stats box
                sect(0, 31, 81, 17)

                # HP
                console.print(2, 33, " " * (math.floor(player.hp / player.hpMax * 77)), bg=RED_L)
                console.print(2 + math.floor(player.hp / player.hpMax * 77), 33, " " * (77 - (math.floor(player.hp / player.hpMax * 77))), bg=RED)
                console.print(37, 33, "HP", fg=WHITE)
                console.print(2, 33, str(player.hp), fg=WHITE)
                console.print(79 - len(str(player.hpMax)), 33, str(player.hpMax), fg=WHITE)

                # MP
                console.print(2, 34, " " * (math.floor(player.mp / player.mpMax * 77)), bg=BLUE_L)
                console.print(2 + math.floor(player.mp / player.mpMax * 77), 34, " " * (77 - (math.floor(player.mp / player.mpMax * 77))), bg=BLUE)
                console.print(37, 34, "MP", fg=WHITE)
                console.print(2, 34, str(player.mp), fg=WHITE)
                console.print(79 - len(str(player.mpMax)), 34, str(player.mpMax), fg=WHITE)

                # EXP
                console.print(2, 35, " " * (math.floor(player.exp / player.lvlup * 77)), bg=AQUA_L)
                console.print(2 + math.floor(player.exp / player.lvlup * 77), 35, " " * (77 - (math.floor(player.exp / player.lvlup * 77))), bg=AQUA)
                console.print(37, 35, "EXP", fg=WHITE)
                console.print(2, 35, str(player.mp), fg=WHITE)
                console.print(79 - len(str(player.mpMax)), 35, str(player.mpMax), fg=WHITE)

                # other
                console.print(2, 36, menu)
                console.print(2, 37, str(select[0]))

                # input box
                sect(0, 47, 81, 3)

                # inventory box
                sect(81, 0, 39, 31)
                console.print(83, 3, "inventory area placeholder")
                console.print(83, 5, "you have like a sharp pointy\nstick or whatever it's called")

                # dice box
                sect(82, 32, 38, 18)
                console.print(83, 31, "|"*(117 - dispwidth))
                console.print(81, 33, "-\n" * 16)

                # print display
                if not menu or re.search("^q:", menu):

                    if activeQuest != "":
                        if questProgress[0] == "END":
                            player.quests["completed"].append(questData["id"])

                            wait = False

                            menu = ""
                            select = [0, 0]
                            menuSelectable = False
                            menuType = "1d"
                            menuAction = ""
                            menuWaiting = ""
                            activeQuest = ""
                            questData = {}
                            questProgress = ["", 0]
                            questSectLen = 0

                            disp("")
                            disp("You finished the quest.")
                            disp("")
                        elif not questProgress[1] > questSectLen:
                            if questNext:
                                disp(questData["content"][questProgress[0]]["content"][questProgress[1]])
                                questNext = False
                                questProgress[1] += 1
                        elif "default" in questData["content"][questProgress[0]]["options"]:
                            if command in ["continue", "c", "ok"]:
                                questProgress[0] = questData["content"][questProgress[0]]["options"]["default"]
                                questProgress[1] = 0
                                command = ""
                        elif command != "":
                            if command in questData["content"][questProgress[0]]["options"]:
                                questProgress[0] = questData["content"][questProgress[0]]["options"][command]
                                questProgress[1] = 0
                            else:
                                disp("That isn't an option")
                            command = ""


                    display_out = [["" * dispwidth] for i in range(dispheight)]
                    while len(display_text) > len(display_out):
                        display_text.pop(0)
                    
                    for line, text in enumerate(display_text):
                        display_out[line] = text.ljust(10)

                    display_blit = []
                    for line in display_out:
                        display_blit.append(''.join(line))

                    console.print(1, 1, "\n".join(display_blit))
                
                else:
                    if menu == "m:inv":
                        items = []
                        shownItems = []
                        for i in getList(select[0], 15, len(player.inv) - 1):
                            if i == None:
                                shownItems.append([None, None])
                            elif player.inv[i] is None:
                                shownItems.append([i, " - "])
                            else:
                                shownItems.append([i, player.inv[i]["name"]])
                            items.append(i)
                        
                        for index, item in enumerate(shownItems):
                            name = item[1]
                            if item[0] is not None:
                                if items[index] == invMove:
                                    color = ORANGE
                                elif items[index] == select[0]:
                                    color = AQUA
                                else:
                                    color = None
                                console.print(2, index * 2 + 1, str(item[0]).rjust(3, " ") + " │ " + name, fg=color)
                                if index + 1 < len(shownItems) and shownItems[index + 1][0] is None:
                                    console.print(2, index * 2 + 2, " ")
                                else:
                                    console.print(2, index * 2 + 2, "    ┼")
                    
                    elif menu == "m:quests":
                        if not questLoading[0] and not questLoading[1]:
                            questLoading[0] = True
                            questLoading[1] = True
                        if questLoading[0]:
                            playableQuests = []
                            for i in questIndex:
                                for j in questIndex[i]:
                                    with open(questIndex[i][j], "r") as file:
                                        questFile = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(file.read())
                                    questUnlocked = True
                                    if questFile["requirements"] == []:
                                        questUnlocked = True
                                    else:
                                        for k in player.quests["completed"]:
                                            if k not in questFile["requirements"]:
                                                questUnlocked = False
                                        if player.quests["completed"] == []:
                                            questUnlocked = False
                                    if questFile["id"] in player.quests["completed"]:
                                        questUnlocked = False
                                    
                                    
                                    if questUnlocked:
                                        playableQuests.append({"name": questFile["title"], "id": re.sub("^q:", "quests:", questFile["id"], 1)})

                            player.quests["available"] = playableQuests
                            questLoading[0] = False
                        
                        else:
                            items = []
                            shownItems = []
                            for i in getList(select[0], 15, len(player.quests["available"])):
                                if i == None:
                                    shownItems.append([None, None])
                                elif player.inv[i] is None:
                                    shownItems.append([i, " - "])
                                else:
                                    shownItems.append([i, player.quests["available"][i]["name"]])
                                items.append(i)
                            
                            for index, item in enumerate(shownItems):
                                name = item[1]
                                if item[0] is not None:
                                    if items[index] == invMove:
                                        color = ORANGE
                                    elif items[index] == select[0]:
                                        color = AQUA
                                    else:
                                        color = None
                                    console.print(2, index * 2 + 1, str(item[0]).rjust(3, " ") + " │ " + name, fg=color)
                                    if index + 1 < len(shownItems) and shownItems[index + 1][0] is None:
                                        console.print(2, index * 2 + 2, " ")
                                    else:
                                        console.print(2, index * 2 + 2, "    ┼")
                    
                    elif re.search("^playQuest:", menu):
                        console.print(2, 2, "Press [Enter] to start quest...")
                        console.print(2, 3, "Press [Esc] to cancel quest...")
                    elif maps.menuContent[menu]["type"] == "1d":
                        items = []
                        shownItems = []
                        for i in getList(select[0], 5, len(maps.menuContent[menu]["items"])):
                            shownItems.append(maps.menuContent[menu]["items"][i])
                            items.append(i)
                        
                        for index, item in enumerate(shownItems):
                            console.print(2, index * 4 + 2, item["text"], fg=AQUA if select[0] == items[index] else None)
                            console.print(1, index * 4 + 4, "-" * 80)
                                    


                # show input text
                if inpFocus:
                    console.print(1, 48, inp+"_")
                else:
                    console.print(1, 48, "░" * 32)
                    console.print(33, 48, "Press / to type")
                    console.print(48, 48, "░" * 32)
            
                # add command to display_text
                if not promptWaiting:
                    if command != "":
                        disp(command)
                        command = ""
                
                # show die info
                if dieSize in maps.dieShape:
                    console.print(83, 33, '\n'.join(maps.dieShape[dieSize]))
                
                if dieSize == 100:
                    console.print(85, 36, str(roll), fg=[0, 255, 0] if not rolling else None)
                elif dieSize:
                    console.print(86, 36, str(roll), fg=[0, 255, 0] if not rolling else None)
                
                if rolling:
                    console.print(83, 40, "█" * math.floor((((11 - rollCount + 1) * 5 + (5 - rollTime)) / 60 * 36)))
                    console.print(83, 41, "Move your mouse to roll.")

                console.print(83, 47, "-" * 36) #maps.border("h", style="thin")
 
                # die labels
                diceLabelLen = 0
                for index, number in enumerate([2, 4, 6, 8, 10, 12, 20, 100]):
                    console.print(83 + diceLabelLen, 48, " " + str(number) + " ", fg=[0, 0, 0] if number == dieSize else None, bg=[0, 255, 0] if number == dieSize else None)
                    diceLabelLen += len(" " + str(number) + " ║")
                    console.print(82 + diceLabelLen, 48, "║")
                
                # roll die
                if rolling:
                    if rollCount > 0:
                        if rollTime <= 0:
                            rollTime = 5
                            rollCount -= 1
                            roll = random.randint(1, dieSize)
                        else:
                            rollTime -= 1
                    else:
                        playing = soundFiles["vine_boom"].play()
                        rolling = False
                        rolled = True
                        rollCount = 0
                        rollTime = 0

            context.present(console)
            console.clear()

            for event in tcod.event.wait() if wait else tcod.event.get():
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, InpAdd):
                    if inpFocus:
                        inp = inp + action.char

                if isinstance(action, Enter):
                    if inpFocus:
                        command = inp
                        inp = ""
                        inpFocus = False
                
                    if state == 0:
                        titlescreen = False
                        wait = True
                        state = 2
                        bg_sound.stop()
                    
                    if menu == "m:inv":
                        if invMove is not None:
                            player.invMove(invMove, select[0])
                            invMove = None
                        else:
                            invMove = select[0]
                    elif menu == "m:quests":
                        questLoading[0] = False
                        questLoading[1] = False
                        quest = player.quests["available"][select[0]]["id"]
                        menu = "playQuest:" + quest
                    elif re.search("^playQuest:", menu):
                        activeQuest = re.sub("^playQuest:quests:", "q:", menu, 1)
                        menu = activeQuest
                        questID = activeQuest.split(":")
                        with open(questIndex[questID[1]][questID[2]]) as questFile:
                            questData = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(questFile.read())
                        questProgress = [questData["entry"], 0]
                        questSectLen = len(questData["content"])
                    elif re.search("^q:", menu):
                        pass
                    elif menu:
                        if re.search("^quit:", maps.menuContent[menu]["items"][select[0]]["target"]):
                            menu = "quit:"
                        elif re.search("^menu:", maps.menuContent[menu]["items"][select[0]]["target"]):
                            menu = re.sub("^menu:", "m:", maps.menuContent[menu]["items"][select[0]]["target"], 1)
                            select[0] = 0
                    
                    if re.search("^q:", menu) and not inpFocus:
                        questNext = True


                if isinstance(action, Backspace):
                    if inpFocus:
                        if len(inp) > 0:
                            inp = inp[:-1]

                if isinstance(action, Arrow):
                    if menu:
                        if menuType in ["1d", "2d"]:
                            if action.direction == "U":
                                select[0] -= 1
                            if action.direction == "D":
                                select[0] += 1
                        if menuType in ["2d"]:
                            if action.direction == "L":
                                select[1] -= 1
                            if action.direction == "R":
                                select[1] += 1
                        
                        if select[0] <= 0:
                            select[0] = 0
                        if menu == "m:inv":
                            menuLength = len(player.inv)
                        elif menu == "m:quests":
                            menuLength = len(player.quests["available"])
                        else:
                            menuLength = len(maps.menuContent[menu]["items"])
                        if select[0] > menuLength - 1:
                            select[0] = menuLength - 1
                
                if isinstance(action, InpToggle):
                    inpFocus = not inpFocus
                    if inpFocus:
                        command = ""
                
                if isinstance(action, RollDie):
                    rolling = True
                    dieSize = action.num
                    rollCount = 11

                elif isinstance(action, EscapeAction):
                    if not menu:
                        menuSelectable = True
                        menuType = "1d"
                        select[0] = 0
                        menu = "m:menu"
                    elif not re.search("^q:", menu):
                        menuSelectable = False
                        menuType = ""
                        menu = ""

"""
 ______ _    _ _   _  _____ _______ _____ ____  _   _  _____ 
|  ____| |  | | \ | |/ ____|__   __|_   _/ __ \| \ | |/ ____|
| |__  | |  | |  \| | |       | |    | || |  | |  \| | (___  
|  __| | |  | | . ` | |       | |    | || |  | | . ` |\___ \ 
| |    | |__| | |\  | |____   | |   _| || |__| | |\  |____) |
|_|     \____/|_| \_|\_____|  |_|  |_____\____/|_| \_|_____/ 
"""

def sect(x, y, w, h, left=True, top=True, right=True, bottom=True, style="double"):
    # top
    console.print(x, y, maps.border("tl" if top and left else "h" if top else "v" if left else None, style))
    console.print(x+1, y, maps.border("h" if top else None, style) * (w-2))
    console.print(x+w-1, y, maps.border("tr" if top and right else "h" if top else "v" if right else None, style))

    # sides
    console.print(x, y+1, (maps.border("v" if left else None, style) + "\n") * (h-2))
    console.print(x+w-1, y+1, (maps.border("v" if right else None, style) + "\n") * (h-2))

    # bottom
    console.print(x, y+h-1, maps.border("bl" if bottom and left else "h" if bottom else "v" if left else None, style))
    console.print(x+1, y+h-1, maps.border("h" if bottom else None, style) * (w-2))
    console.print(x+w-1, y+h-1, maps.border("br" if bottom and right else "h" if bottom else "v" if right else None, style))

def disp(string):
    global display_text
    if string == "":
        display_text.append("")
    else:
        txt = textwrap.wrap(string)
        display_text += txt

def getList(index, amount, total): # amount is amount displayed, total is the total amount of items in list
    indexList = []
    if amount == total:
        return [i for i in range(amount)]

    if amount >= total:
        return [i for i in range(total)] + [None for j in range(amount - total)] 
    else:
        indexList = [i for i in range(index - math.ceil(amount / 2), index + math.floor(amount / 2))]
    
    for i, v in enumerate(indexList):
        if indexList[i] < 0:
            indexList[i] = None
        elif indexList[i] > total:
            indexList[i] = None
    
    return indexList
    

def showQuestList():
    menu = "m:quests"

if __name__ == "__main__":
    main()