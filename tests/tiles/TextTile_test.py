from blessed import Terminal
from blessedui import TileSubject, tiles
from tests import TestCase


class TextTileTestCase(TestCase):
    def test_render(self):
        terminal = Terminal()
        subject = TileSubject('Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        tile = tiles.TextTile(subject=subject, title='Title', withBorders=False)

        result = tile.render(terminal=terminal, width=28, height=5)

        self.assertEqual([
            'Lorem ipsum dolor sit amet, ',
            'consectetur adipiscing elit.',
        ], result)
