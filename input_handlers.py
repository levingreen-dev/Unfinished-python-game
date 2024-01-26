from typing import Optional

import tcod.event

from actions import *
from keys import keys


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key in keys.keyStr:
            action = InpAdd(key)

        if key in keys.numKeys:
            action = RollDie(key)

        if key == tcod.event.K_SLASH:
            action = InpToggle()
        
        if key == tcod.event.K_RETURN:
            action = Enter()

        if key == tcod.event.K_BACKSPACE:
            action = Backspace()

        if key in keys.arrows:
            action = Arrow(key)

        if key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action