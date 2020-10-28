from typing import List

from blessedui.stringutils import escape_ansi
from blessedui.exceptions import FrameException


class Frame:
    _lines: List[str]

    def __init__(self):
        object.__setattr__(self, '_lines', [])

    @property
    def lines(self) -> List[str]:
        return self._lines

    @lines.setter
    def lines(self, value):
        raise FrameException('Please use the render function')

    def fillLine(self, line: str, width: int, char: str = ' ') -> str:
        '''
        Fill an unterminated line with spaces.
        Automatically used when a render process is been fired.
        '''
        if len(char) != 1:
            raise FrameException(
                f'"char" parameter must be a single character (found: "{char}")')

        escaped = escape_ansi(line)
        lineLen = len(escaped)
        if lineLen >= width:
            return line

        return line + (char * (width - lineLen))

    def fillEmptyLines(self, width: int, height: int, rightExtra: str = '', leftExtra: str = ''):
        '''
        Fill the remaining lines with spaces.
        Automatically used when a render process is been fired.
        '''
        linesLen = len(self._lines)

        if linesLen >= height:
            return

        for _ in range(height - linesLen):
            self._lines.append(leftExtra + self.fillLine('', width) + rightExtra)
