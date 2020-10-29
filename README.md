# BlessedUI

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Codecov](https://img.shields.io/codecov/c/github/elegos/python-blessedui?token=Q5LZ19E2Z7)](https://codecov.io/gh/elegos/python-blessedui/)

This is a python graphic library based on the [blessed](https://pypi.org/project/blessed/) project.

Initially inspired by [Federico Ceratto's Dashing](https://github.com/FedericoCeratto/dashing), the key difference is a multi-thread, observer pattern, class-first approach to make terminal interfaces as easy as possible.

## Example usage
```python
from blessedui import BlessedUI, TileSubject, tiles
from time import sleep

# TileSubject are generic-typed observer pattern subjects,
# which can be easily updated by calling themselves.
# Their type depends on the constructor's argument.
# Each tile should specify a non-generic TileSubject.
textSubject1 = TileSubject('Text subject 1')
textSubject2 = TileSubject('Text subject 2')
textSubject3 = TileSubject('Text subject 3')

# BlessedUI is like the body of an HTML document,
# while the tiles are block-like elements, taking the full width of the view.
ui = BlessedUI(
    tiles.TextTile(subject=textSubject1,  withBorders=False, title='Unbordered text tile'),
    # The SplitTile takes other tiles as arguments, producing an equally vertically
    # split view
    tiles.SplitTile(
        tiles.TextTile(subject=textSubject2, withBorders=True, title='Split 1'),
        tiles.TextTile(subject=textSubject3, withBorders=True, title='Split 2'),
        tiles.TextTile(subject=textSubject2, withBorders=True, title='Split 3'),
    ),
)

# The UI runs in an asynchronous thread, letting the application's logics
# run in the main thread, simplifying the writing of the main file.
ui.run()

# Application's logics
sleep(3)
# To update a TileSubject, just call it again with the new content.
# The UI will refresh only if any of the subjects change.
# The single tiles will refresh their graphic representation only if their subject will change.
textSubject1('Cool stuff')
textSubject2('Change me')
textSubject3('A sentence')

# Stop the UI
ui.stop()
# Await the UI's thread to stop
ui.join()

```

## Extending (creating new tiles)

The library is made to be easily enhanced with new tiles.

To create a new tile, you need to extend the `blessedui.Tile` class and implement its abstract `render` method.

See the [tile.py](src/blessedui/tile.py) file to see the rest of the overrideable methods.

See [tiles.py](src/blessedui/tiles.py) for a list of available tiles.

```python
from typing import List

from blessed import Terminal
from blessedui import Tile, TileSubject


class StringsListTile(Tile[List[str]]):
    def render(self, terminal: Terminal, width: int, height: int) -> List[str]:
        result: List[str] = self.subject # self.subject is a list of strings, as per tile's type

        return result
```
