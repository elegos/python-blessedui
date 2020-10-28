from typing import List
from unittest.mock import Mock

import blessed
from blessedui import BlessedUI, Tile, TileSubject
from unittest_data_provider import data_provider

from tests import DumbTile, TestCase


class BlessedUITestCase(TestCase):
    @data_provider(lambda: [
        [[], {'terminal': None, 'maxRefreshRate': 1}, 0, 1.00],
        [[DumbTile(TileSubject('')), DumbTile(TileSubject(''))], {
            'terminal': None,
            'maxRefreshRate': 30
        }, 2, 0.0333333],
    ])
    def test_init(self, tiles: List[Tile], kwargs: dict, expectedTilesLen, expectedFrameDuration):
        ui = BlessedUI(*tiles, **kwargs)
        self.assertIsInstance(ui.terminal, blessed.Terminal)
        self.assertLen(expectedTilesLen, ui.tiles, f'There should be {expectedTilesLen} files')
        self.assertAlmostEqual(
            expectedFrameDuration,
            ui.frameDuration,
            msg=f'Frame duration should be {expectedFrameDuration}'
        )

    def test_start_stop(self):
        # Return True once, then False
        def shouldRender(mockObj: Mock):
            def inner():
                mockObj.shouldRender.side_effect = lambda: False
                return True

            return inner

        tile1 = Mock()
        tile1.shouldRender = Mock(side_effect=shouldRender(tile1))
        tile1.lines = ['']

        tile2 = Mock()
        tile2.shouldRender = Mock(side_effect=shouldRender(tile2))
        tile2.lines = ['']

        ui = BlessedUI(tile1, tile2)
        self.assertIsNone(ui._thread,
                          msg="Before starting it, the UI's thread should not exist")

        ui.run()
        self.assertTrue(ui._thread.is_alive(),
                        msg="After starting it, the UI's thread should be running")

        ui.run()
        self.assertTrue(ui._thread.is_alive(),
                        msg="After re-starting it, the UI's thread should still be running")

        ui.stop()
        # Await the async process to stop
        ui.join()
        self.assertFalse(ui._thread.is_alive(),
                         msg="After stopping it, the UI's thread should not be running")
        self.assertEqual(1, tile1.refresh.call_count,
                         "After running multiple times, the tile1's refresh method should have been called once")  # noqa E501
        self.assertEqual(1, tile2.refresh.call_count,
                         "After running multiple times, the tile2's refresh method should have been called once")  # noqa E501
