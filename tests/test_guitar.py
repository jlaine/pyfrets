import re
import unittest

from pyfrets.guitar import Cell, Fretboard, Orientation


def strip_ansi(v: str) -> str:
    return re.sub(r"\033\[\d+m", "", v)


class GuitarTest(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.fretboard = Fretboard()
        self.fretboard.set((1, 0), Cell(color="red", text="X"))
        self.fretboard.set((2, 0), Cell(color="red", text="YY"))
        self.fretboard.set((3, 0), Cell(color="red", text="ZZZ"))

    def test_dump_ansi(self) -> None:
        self.assertEqual(
            strip_ansi(self.fretboard.dump_ansi(orientation=Orientation.PORTRAIT)),
            """00  |    |    |    |    |    | 
   ============================
01  X    |    |    |    |    | 
   ----------------------------
02  YY   |    |    |    |    | 
   ----------------------------
03 ZZZ   |    |    |    |    | 
   ----------------------------
04  |    |    |    |    |    | 
   ----------------------------
05  |    |    |    |    |    | 
   ----------------------------
06  |    |    |    |    |    | 
   ----------------------------
07  |    |    |    |    |    | 
   ----------------------------
08  |    |    |    |    |    | 
   ----------------------------
09  |    |    |    |    |    | 
   ----------------------------
10  |    |    |    |    |    | 
   ----------------------------
11  |    |    |    |    |    | 
   ----------------------------
12  |    |    |    |    |    | 
   ----------------------------
13  |    |    |    |    |    | 
   ----------------------------
14  |    |    |    |    |    | 
   ----------------------------
15  |    |    |    |    |    | 
   ----------------------------
""",  # noqa: W291
        )

        self.assertEqual(
            strip_ansi(self.fretboard.dump_ansi(orientation=Orientation.LANDSCAPE)),
            """---||---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
---||---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
---||---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
---||---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
---||---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
---||-X-|-YY|ZZZ|---|---|---|---|---|---|---|---|---|---|---|---|
00   01  02  03  04  05  06  07  08  09  10  11  12  13  14  15  
""",  # noqa: W291
        )

    def test_dump_svg(self) -> None:
        self.assertEqual(
            self.fretboard.dump_svg(orientation=Orientation.PORTRAIT),
            """<svg viewBox="0 0 140 500" xmlns="http://www.w3.org/2000/svg">
<g transform="translate(20, 0)">
<line x1="10" y1="10" x2="10" y2="490" stroke="black"/>
<line x1="30" y1="10" x2="30" y2="490" stroke="black"/>
<line x1="50" y1="10" x2="50" y2="490" stroke="black"/>
<line x1="70" y1="10" x2="70" y2="490" stroke="black"/>
<line x1="90" y1="10" x2="90" y2="490" stroke="black"/>
<line x1="110" y1="10" x2="110" y2="490" stroke="black"/>
<line x1="10" y1="10" x2="110" y2="10" stroke="black" stroke-width="1"/>
<line x1="10" y1="40" x2="110" y2="40" stroke="black" stroke-width="2"/>
<line x1="10" y1="70" x2="110" y2="70" stroke="black" stroke-width="1"/>
<line x1="10" y1="100" x2="110" y2="100" stroke="black" stroke-width="1"/>
<line x1="10" y1="130" x2="110" y2="130" stroke="black" stroke-width="1"/>
<line x1="10" y1="160" x2="110" y2="160" stroke="black" stroke-width="1"/>
<line x1="10" y1="190" x2="110" y2="190" stroke="black" stroke-width="1"/>
<line x1="10" y1="220" x2="110" y2="220" stroke="black" stroke-width="1"/>
<line x1="10" y1="250" x2="110" y2="250" stroke="black" stroke-width="1"/>
<line x1="10" y1="280" x2="110" y2="280" stroke="black" stroke-width="1"/>
<line x1="10" y1="310" x2="110" y2="310" stroke="black" stroke-width="1"/>
<line x1="10" y1="340" x2="110" y2="340" stroke="black" stroke-width="1"/>
<line x1="10" y1="370" x2="110" y2="370" stroke="black" stroke-width="1"/>
<line x1="10" y1="400" x2="110" y2="400" stroke="black" stroke-width="1"/>
<line x1="10" y1="430" x2="110" y2="430" stroke="black" stroke-width="1"/>
<line x1="10" y1="460" x2="110" y2="460" stroke="black" stroke-width="1"/>
<line x1="10" y1="490" x2="110" y2="490" stroke="black" stroke-width="1"/>
<text x="-10" y="29" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 25)">0</text>
<text x="-10" y="59" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 55)">1</text>
<circle cx="10" cy="55" r="8" stroke="red" fill="white"/>
<text x="10" y="59" fill="red" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, 10, 55)">X</text>
<text x="-10" y="89" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 85)">2</text>
<circle cx="10" cy="85" r="8" stroke="red" fill="white"/>
<text x="10" y="89" fill="red" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, 10, 85)">YY</text>
<text x="-10" y="119" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 115)">3</text>
<circle cx="10" cy="115" r="8" stroke="red" fill="white"/>
<text x="10" y="119" fill="red" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, 10, 115)">ZZZ</text>
<text x="-10" y="149" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 145)">4</text>
<text x="-10" y="179" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 175)">5</text>
<text x="-10" y="209" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 205)">6</text>
<text x="-10" y="239" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 235)">7</text>
<text x="-10" y="269" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 265)">8</text>
<text x="-10" y="299" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 295)">9</text>
<text x="-10" y="329" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 325)">10</text>
<text x="-10" y="359" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 355)">11</text>
<text x="-10" y="389" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 385)">12</text>
<text x="-10" y="419" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 415)">13</text>
<text x="-10" y="449" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 445)">14</text>
<text x="-10" y="479" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(0, -10, 475)">15</text>
</g>
</svg>
""",  # noqa: E501,
        )
        self.assertEqual(
            self.fretboard.dump_svg(orientation=Orientation.LANDSCAPE),
            """<svg viewBox="0 0 500 140" xmlns="http://www.w3.org/2000/svg">
<g transform="translate(0, 120) rotate(-90, 0, 0)">
<line x1="10" y1="10" x2="10" y2="490" stroke="black"/>
<line x1="30" y1="10" x2="30" y2="490" stroke="black"/>
<line x1="50" y1="10" x2="50" y2="490" stroke="black"/>
<line x1="70" y1="10" x2="70" y2="490" stroke="black"/>
<line x1="90" y1="10" x2="90" y2="490" stroke="black"/>
<line x1="110" y1="10" x2="110" y2="490" stroke="black"/>
<line x1="10" y1="10" x2="110" y2="10" stroke="black" stroke-width="1"/>
<line x1="10" y1="40" x2="110" y2="40" stroke="black" stroke-width="2"/>
<line x1="10" y1="70" x2="110" y2="70" stroke="black" stroke-width="1"/>
<line x1="10" y1="100" x2="110" y2="100" stroke="black" stroke-width="1"/>
<line x1="10" y1="130" x2="110" y2="130" stroke="black" stroke-width="1"/>
<line x1="10" y1="160" x2="110" y2="160" stroke="black" stroke-width="1"/>
<line x1="10" y1="190" x2="110" y2="190" stroke="black" stroke-width="1"/>
<line x1="10" y1="220" x2="110" y2="220" stroke="black" stroke-width="1"/>
<line x1="10" y1="250" x2="110" y2="250" stroke="black" stroke-width="1"/>
<line x1="10" y1="280" x2="110" y2="280" stroke="black" stroke-width="1"/>
<line x1="10" y1="310" x2="110" y2="310" stroke="black" stroke-width="1"/>
<line x1="10" y1="340" x2="110" y2="340" stroke="black" stroke-width="1"/>
<line x1="10" y1="370" x2="110" y2="370" stroke="black" stroke-width="1"/>
<line x1="10" y1="400" x2="110" y2="400" stroke="black" stroke-width="1"/>
<line x1="10" y1="430" x2="110" y2="430" stroke="black" stroke-width="1"/>
<line x1="10" y1="460" x2="110" y2="460" stroke="black" stroke-width="1"/>
<line x1="10" y1="490" x2="110" y2="490" stroke="black" stroke-width="1"/>
<text x="-10" y="29" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 25)">0</text>
<text x="-10" y="59" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 55)">1</text>
<circle cx="10" cy="55" r="8" stroke="red" fill="white"/>
<text x="10" y="59" fill="red" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, 10, 55)">X</text>
<text x="-10" y="89" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 85)">2</text>
<circle cx="10" cy="85" r="8" stroke="red" fill="white"/>
<text x="10" y="89" fill="red" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, 10, 85)">YY</text>
<text x="-10" y="119" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 115)">3</text>
<circle cx="10" cy="115" r="8" stroke="red" fill="white"/>
<text x="10" y="119" fill="red" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, 10, 115)">ZZZ</text>
<text x="-10" y="149" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 145)">4</text>
<text x="-10" y="179" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 175)">5</text>
<text x="-10" y="209" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 205)">6</text>
<text x="-10" y="239" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 235)">7</text>
<text x="-10" y="269" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 265)">8</text>
<text x="-10" y="299" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 295)">9</text>
<text x="-10" y="329" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 325)">10</text>
<text x="-10" y="359" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 355)">11</text>
<text x="-10" y="389" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 385)">12</text>
<text x="-10" y="419" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 415)">13</text>
<text x="-10" y="449" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 445)">14</text>
<text x="-10" y="479" font-family="arial" font-size="12px" text-anchor="middle" transform="rotate(90, -10, 475)">15</text>
</g>
</svg>
""",  # noqa: E501
        )

    def test_walk(self) -> None:
        cells = list(self.fretboard.walk())
        self.assertEqual(len(cells), 96)
