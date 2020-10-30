from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from blessed import Terminal

from blessedui.frame import Frame
from blessedui.stringutils import escape_ansi

T = TypeVar('T')


class SubjectObserver(Generic[T], ABC):
    @abstractmethod
    def update(self, subject: T) -> None:
        pass


class TileSubject(Generic[T]):
    def __init__(self, value: T):
        self._value = value
        self._subscribers: List[SubjectObserver[T]] = []

    def subscribe(self, observer: SubjectObserver[T]):
        if observer not in self._subscribers:
            self._subscribers.append(observer)

    def unsubscribe(self, observer: SubjectObserver[T]):
        if observer in self._subscribers:
            self._subscribers.remove(observer)

    def __call__(self, value: T):
        self._value = value
        for observer in self._subscribers:
            observer.update(self._value)


class Tile(SubjectObserver[T], Frame):
    subject: T
    title: str

    borderTopLeft = u'┌'
    borderTopRight = '┐'
    borderBottomLeft = u'└'
    borderBottomRight = u'┘'
    borderTop = '─'
    borderBottom = '─'
    borderLeft = '│'
    borderRight = '│'

    def __init__(self, subject: TileSubject[T], title: str = '', withBorders: bool = False):
        self._bordered = withBorders
        self.title = title

        Frame.__init__(self)

        subject.subscribe(self)
        self._shouldRender = True
        self.subject = subject._value
        self._subscribers: List[SubjectObserver[List[str]]] = []

    def update(self, subject: T) -> None:
        '''
        Observer pattern. Update the subject's value upon observed changed it.
        '''
        shouldRender = self.subject != subject
        self.subject = subject
        self._shouldRender = shouldRender

    def refresh(self, terminal: Terminal, width: int, height: int) -> None:
        '''
        Trigger a tile's refresh (render), decorating it with eventual borders

        terminal : Terminal
          The instance of blessedui's Terminal
        subject : T
          The data to be displayed
        width : int
          The available width
        height : int
          The available height
        '''
        if not self.shouldRender():
            return

        self._lines.clear()
        left = ''
        right = ''

        titled = len(self.title) > 0
        if self._bordered or titled:
            topLine = terminal.normal + (self.borderTopLeft if self._bordered else ' ')
            topLine += (self.borderTop if self._bordered else ' ')*4
            if titled:
                topLine += f'   {self.title}   '
            topLine = self.fillLine(line=topLine, width=width - 1,
                                    char=self.borderTop if self._bordered else ' ')
            topLine += self. borderTopRight if self._bordered else ' '
            self._lines.append(topLine)
            if self._bordered:
                left = terminal.normal + self.borderLeft
                right = terminal.normal + self.borderRight

        fillWidth = width - len(escape_ansi(left)) - len(escape_ansi(right))
        linesNum = height
        linesToRender = height
        if self.title != '':
            linesNum = height - 1
            linesToRender -= 1
        if self._bordered:
            linesNum = height - 1
            linesToRender -= 1

        self._lines.extend([
            left + self.fillLine(line=line, width=fillWidth) + right
            for line in self.render(
                terminal=terminal,
                width=fillWidth,
                height=linesToRender,
            )
        ])
        self.fillEmptyLines(
            width=fillWidth,
            height=height if not self._bordered else linesNum,
            leftExtra=left,
            rightExtra=right,
        )

        if self._bordered:
            bottomLine = terminal.normal + self.borderBottomLeft
            bottomLine = self.fillLine(line=bottomLine, width=width - 2,
                                       char=self.borderBottom) + self.borderBottom
            bottomLine += self.borderBottomRight
            self._lines.append(bottomLine)

        self._shouldRender = False

    def shouldRender(self) -> bool:
        return self.subject is not None and self._shouldRender

    @abstractmethod
    def render(self, terminal: Terminal, width: int, height: int) -> List[str]:
        '''
        You can use self.terminal to use blessed capabilities, self.subject to get the data.

        terminal : Terminal
          The instance of blessedui's Terminal
        width : int
          The available width
        height : int
          The available height
        '''
        pass
