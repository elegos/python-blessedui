from functools import reduce
from math import floor
from typing import List

from blessed import Terminal

from blessedui.tile import Tile, TileSubject


class SplitTile(Tile):
    '''
    Split the horizontal space equally between different sub-tiles
    '''
    tiles: List[Tile]

    def __init__(self, *tiles: Tile):
        super(SplitTile, self).__init__(subject=TileSubject(''), title='', withBorders=False)
        self.tiles = list(tiles)

    def shouldRender(self) -> bool:
        return reduce(lambda x, y: x or y, [tile.shouldRender() for tile in self.tiles], False)

    def render(self, terminal: Terminal, width: int, height: int) -> List[str]:
        subtileWidth = floor(width / len(self.tiles))
        tileLines: List[List[str]] = []
        for tile in self.tiles:
            tile.refresh(terminal=terminal, width=subtileWidth, height=height)
            tileLines.append(tile.lines)

        lines: List[str] = []

        for i in range(height):
            line = ''
            for j in range(len(self.tiles)):
                line += (
                    tileLines[j][i] if len(tileLines[j]) > i
                    else self.fillLine(line='', width=subtileWidth, char=' ')
                )

            lines.append(self.fillLine(line=line, width=width, char=' '))

        return lines


class TextTile(Tile[str]):
    def render(self, terminal: Terminal, width: int, height: int) -> List[str]:
        lines = []
        splitLines: List[str] = self.subject.split('\n')
        for line in splitLines:
            for i in range(0, len(line), width):
                lines.append(line[i:i + width])

        return lines[0:height]
