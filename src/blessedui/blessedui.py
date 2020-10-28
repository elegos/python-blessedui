from datetime import datetime
from math import floor
from threading import Thread
from time import sleep
from typing import List, Optional

from blessed import Terminal

from blessedui.tile import Tile
from functools import reduce


class BlessedUI:
    terminal: Terminal
    tiles: List[Tile]
    frameDuration: float

    def __init__(self, *tiles: Tile, terminal: Terminal = None, maxRefreshRate: int = 30):
        '''
        terminal : Terminal
            A blessedui.Terminal instance. A new one is created if not specified.
        maxRefreshRate : int
            The maximum refresh rate the application should run at, expressed
            in hertz (hz). 30 hz by default.
        tiles: List[Tile]
            The list of tiles the UI must handle, each displayed at the bottom of the previous one.
        '''
        self.terminal = terminal if terminal is not None else Terminal()
        self.frameDuration = 1.0/maxRefreshRate
        self.tiles = list(tiles)
        self._thread: Optional[Thread] = None
        self._run = False

    def run(self) -> None:
        '''
        Start displaying the UI.
        Non-blocking action.
        '''

        if self._thread is not None and self._thread.is_alive():
            self._run = False
            self._thread.join()

        self._thread = Thread(daemon=True, target=self._render)
        self._run = True
        self._thread.start()

    def stop(self, clearScreen: bool = True) -> None:
        '''
        Stop rendering the UI.
        clearScreen : bool
            If True, print empty spaces across the whole screen
        '''
        self._run = False
        if clearScreen:
            for _ in range(self.terminal.height):
                print(self.terminal.normal + ' ' * self.terminal.width)

    def _render(self):
        while self._run:
            beforeRender = datetime.now()

            numTiles = len(self.tiles)
            width = self.terminal.width
            height = floor((self.terminal.height - 1) / (numTiles if numTiles > 0 else 1))
            shouldRender = reduce(lambda x, y: x or y, [
                tile.shouldRender() for tile in self.tiles
            ], False)

            if shouldRender:
                for tile in self.tiles:
                    tile.refresh(terminal=self.terminal, width=width, height=height)
                    for line in tile.lines:
                        print(line)
                # Fill eventual ending lines
                for _ in range(self.terminal.height - height * len(self.tiles) - 2):
                    print(' ' * width)

            afterRender = datetime.now()
            waitSeconds = self.frameDuration - (
                (afterRender - beforeRender).microseconds / 10000.0
            )
            if waitSeconds > 0:
                sleep(waitSeconds)

    def join(self) -> None:
        '''
        Await the render process to finish.
        ATTENTION: it might take forever, if BlessedUI.stop() is not been called.
        '''
        if self._thread is not None:
            self._thread.join()
