from unittest import TestCase

from blessedui import Frame
from blessedui.exceptions import FrameException


class FrameTestCase(TestCase):
    def test_lines_prop_write(self):
        frame = Frame()
        with self.assertRaises(
            FrameException,
            msg="You shouldn't be able to set the frame's lines directly"
        ):
            frame.lines = []

    def test_lines_prop_read(self):
        frame = Frame()
        frame._lines.extend(['whenever', 'wherever'])

        self.assertEqual(['whenever', 'wherever'], frame.lines)

    def test_fillLine(self):
        frame = Frame()
        self.assertEqual('foo~~', frame.fillLine(line='foo', width=5, char='~'))
        self.assertEqual('foo--', frame.fillLine(line='foo--', width=5, char='~'))

    def test_fillLine_wrong_char_length(self):
        frame = Frame()
        with self.assertRaises(
            FrameException,
            msg='Only 1-character long string should be allowed to be used as fill char'
        ):
            frame.fillLine(line='', width=1, char='12')

    def test_fillEmptyLines(self):
        frame = Frame()
        frame._lines = ['line 1']

        frame.fillEmptyLines(width=5, height=1, rightExtra='', leftExtra='')
        self.assertEqual(1, len(frame.lines), 'Filling 1 line should produce a list of 1 lines')

        frame.fillEmptyLines(width=5, height=5, rightExtra='~', leftExtra='|')
        self.assertEqual([
            'line 1', '|     ~', '|     ~', '|     ~', '|     ~'
        ], frame.lines)
