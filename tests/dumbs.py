from typing import List, TypeVar

from blessed import Terminal
from blessedui import Tile, TileSubject

T = TypeVar('T')


class DumbTile(Tile[T]):
    def __init__(
        self, subject: TileSubject[T], title: str = '',
        withBorders: bool = False, shouldRender: bool = True,
    ):
        super(DumbTile, self).__init__(subject=subject, title=title, withBorders=withBorders)
        self._shouldRender = shouldRender

    def render(self, terminal: Terminal, width: int, height: int) -> List[str]:
        return [self.subject]
