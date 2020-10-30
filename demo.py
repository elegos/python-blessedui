from blessedui import BlessedUI, TileSubject, tiles
from time import sleep
import lorem

textSubject1 = TileSubject(lorem.sentence())
textSubject2 = TileSubject(lorem.sentence())
textSubject3 = TileSubject(lorem.sentence())
textSubject4 = TileSubject(lorem.sentence())
textSubject5 = TileSubject(lorem.sentence())

ui = BlessedUI(
    tiles.TextTile(subject=textSubject1,  withBorders=False, title='Whenever'),
    tiles.SplitTile(
        tiles.TextTile(subject=textSubject2, withBorders=True, title='Split 1'),
        tiles.TextTile(subject=textSubject3, withBorders=True, title='Split 2'),
        tiles.TextTile(subject=textSubject4, withBorders=True, title='Split 3'),
        tiles.TextTile(subject=textSubject5, withBorders=True, title='Split 4'),
    ),
)

ui.run()

while True:
    sleep(3)
    textSubject1(lorem.paragraph())
    textSubject2(lorem.paragraph())
    textSubject3(lorem.paragraph())
    textSubject4(lorem.paragraph())
    textSubject5(lorem.paragraph())

ui.join()
