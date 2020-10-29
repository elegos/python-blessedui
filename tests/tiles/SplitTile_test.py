import math
from typing import List
from unittest.mock import Mock

import blessed
from blessedui import Tile, TileSubject, tiles
from tests import DumbTile, TestCase
from unittest_data_provider import data_provider


class SplitTileTestCase(TestCase):
    def test_init(self):
        tile = tiles.SplitTile(1, 2, 3)
        self.assertEqual([1, 2, 3], tile.tiles)

    @data_provider(lambda: [
        [[
            DumbTile(subject=TileSubject(''), shouldRender=False),
            DumbTile(subject=TileSubject(''), shouldRender=False),
            DumbTile(subject=TileSubject(''), shouldRender=True)
        ], True],
        [[DumbTile(subject=TileSubject(''), shouldRender=True)], True],
        [[DumbTile(subject=TileSubject(''), shouldRender=False)], False],
    ])
    def test_shouldRender(self, dumbTiles: List[Tile], shouldRender: bool):
        tile = tiles.SplitTile(*dumbTiles)
        self.assertEqual(shouldRender, tile.shouldRender())

    def test_render(self):
        terminal = blessed.Terminal
        width = 80
        height = 40

        tile1 = Mock()
        tile2 = Mock()
        tile3 = Mock()

        tile1.refresh = Mock()
        tile2.refresh = Mock()
        tile3.refresh = Mock()

        tile1.lines = ['line1']
        tile2.lines = ['line2']
        tile3.lines = ['line3']

        expectedWidth = math.floor(width / 3)
        expectedHeight = height
        expectedOutput = [
            (
                tile1.lines[0] +
                tile2.lines[0] +
                tile3.lines[0] +
                (' '*(width - len(tile1.lines[0]) -
                      len(tile2.lines[0]) - len(tile3.lines[0])))
            ),
            *[' '*width for _ in range(expectedHeight - 1)]
        ]

        tile = tiles.SplitTile(tile1, tile2, tile3)
        output = tile.render(terminal=terminal, width=width, height=height)

        self.assertEqual(expectedOutput, output)

        for t in [tile1, tile2, tile3]:
            self.assertEqual(1, t.refresh.call_count,
                             "Each tile's refresh method should be called once")
            tile1.refresh.assert_called_with(
                terminal=terminal, width=expectedWidth, height=expectedHeight)
