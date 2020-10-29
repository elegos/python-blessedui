from unittest import TestCase
from unittest.mock import Mock

from blessed import Terminal
from blessedui import TileSubject

from tests import DumbTile


class TileTestCase(TestCase):
    def test_tilesubject_subscribe_unsubscribe(self):
        subject = TileSubject('')
        observer = Mock()

        subject.subscribe(observer)
        subject('change 1')
        subject.unsubscribe(observer)
        subject('change 2')

        observer.update.assert_called_with('change 1')
        self.assertEqual(1, observer.update.call_count,
                         'The observer should be called only when subscribed')

    def test_init(self):
        tile = DumbTile(subject=TileSubject('test'), title='title', withBorders=True)
        self.assertEqual('title', tile.title)
        self.assertEqual('test', tile.subject)
        self.assertEqual([], tile.lines)

    def test_update(self):
        tile = DumbTile(subject=TileSubject('foo'))

        tile.update('foo')
        self.assertFalse(tile.shouldRender())
        self.assertEqual('foo', tile.subject)

        tile.update('bar')
        self.assertTrue(tile.shouldRender())
        self.assertEqual('bar', tile.subject)

    def test_refresh_with_borders(self):
        terminal = Terminal()
        tile = DumbTile(subject=TileSubject('foo'), title='bar', withBorders=True)
        tile.refresh(terminal=terminal, width=19, height=5)
        self.assertEqual([
            '┌────   bar   ────┐',
            '│foo              │',
            '│                 │',
            '│                 │',
            '└─────────────────┘',
        ], tile.lines)

    def test_refresh_without_borders(self):
        terminal = Terminal()
        tile = DumbTile(subject=TileSubject('foo'), title='bar', withBorders=False)
        tile.refresh(terminal=terminal, width=19, height=5)
        self.assertEqual([
            '        bar        ',
            'foo                ',
            '                   ',
            '                   ',
            '                   ',
        ], tile.lines)
