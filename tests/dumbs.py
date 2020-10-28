from typing import List

from blessed import Terminal
from blessedui import Tile


class DumbTile(Tile):
    def render(self, terminal: Terminal, width: int, height: int) -> List[str]:
        return [self.subject]
