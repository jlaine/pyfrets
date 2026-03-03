import dataclasses
import enum
from typing import Iterator

from colorama import Back, Fore, Style

FRETS = 16
STRINGS = [
    40,  # E2
    45,  # A2
    50,  # D3
    55,  # G3
    59,  # B3
    64,  # E4
]


@dataclasses.dataclass
class Cell:
    color: str
    text: str


class Orientation(enum.Enum):
    PORTRAIT = "PORTRAIT"
    LANDSCAPE = "LANDSCAPE"


def pad(i: str, p: str) -> str:
    if len(i) == 1:
        return p + i + p
    elif len(i) == 2:
        return p + i
    else:
        return i


class Fretboard:
    def __init__(self) -> None:
        self._cells: list[list[Cell | None]] = [
            [None for x in STRINGS] for f in range(FRETS)
        ]

    def dump_ansi(self, *, orientation: Orientation) -> str:
        """
        Write to an ANSI string.
        """
        if orientation == Orientation.LANDSCAPE:
            return self._dump_ansi_landscape()
        else:
            return self._dump_ansi_portrait()

    def _dump_ansi_landscape(self) -> str:
        lines = []
        empty_line = "   ||" + ("   |" * (FRETS - 1))
        for string_idx in range(len(STRINGS) - 1, -1, -1):
            cells = [row[string_idx] for row in self._cells]
            line = "".join(
                (
                    getattr(Fore, cell.color.upper()) + pad(cell.text, "-")
                    if cell is not None
                    else (Fore.BLACK + pad("-", "-"))
                )
                + Fore.BLACK
                + ("|" if idx else "||")
                for idx, cell in enumerate(cells)
            )
            lines.append(Back.WHITE + line)
            if string_idx:
                lines.append(Back.WHITE + Fore.BLACK + empty_line)
            else:
                lines.append(
                    Fore.WHITE
                    + "".join([f"{i:02}  " + ("" if i else " ") for i in range(FRETS)])
                )
        return "".join(line + Style.RESET_ALL + "\n" for line in lines)

    def _dump_ansi_portrait(self) -> str:
        indent = "   "
        lines = []
        width = 5 * len(STRINGS) - 2
        for idx, row in enumerate(self._cells):
            line = "  ".join(
                (
                    (getattr(Fore, cell.color.upper()) + pad(cell.text, " "))
                    if cell is not None
                    else (Fore.BLACK + pad("|", " "))
                )
                for cell in row
            )
            lines.append(f"{idx:02} " + Back.WHITE + line)
            marker = "-" if idx else "="
            lines.append(indent + Back.WHITE + Fore.BLACK + (marker * width))
        return "".join(line + Style.RESET_ALL + "\n" for line in lines)

    def dump_svg(self, *, orientation: Orientation) -> str:
        """
        Write the fretboard to an SVG image.
        """
        font_family = "arial"
        font_size = "12px"
        padding = 10
        fret_spacing = 30
        string_spacing = 20
        circle_radius = 8
        board_width = string_spacing * (len(STRINGS) - 1)
        board_height = fret_spacing * FRETS
        image_width = board_width + 4 * padding
        image_height = board_height + 2 * padding

        if orientation == Orientation.LANDSCAPE:
            svg_transform = (
                f"translate(0, {image_width - 2 * padding}) rotate(-90, 0, 0)"
            )
            svg_viewbox = f"0 0 {image_height} {image_width}"
            text_angle = 90
        else:
            svg_transform = f"translate({2 * padding}, 0)"
            svg_viewbox = f"0 0 {image_width} {image_height}"
            text_angle = 0

        output = [
            f'<svg viewBox="{svg_viewbox}" xmlns="http://www.w3.org/2000/svg">',
            f'<g transform="{svg_transform}">',
        ]

        # Draw strings
        for string_idx, string_note in enumerate(STRINGS):
            x = padding + string_idx * string_spacing
            output.append(
                f'<line x1="{x}" y1="{padding}"'
                f' x2="{x}" y2="{padding + board_height}" stroke="black"/>'
            )

        # Draw frets.
        for fret_idx in range(FRETS + 1):
            y = padding + fret_idx * fret_spacing
            output.append(
                f'<line x1="{padding}" y1="{y}"'
                f' x2="{padding + board_width}" y2="{y}"'
                f' stroke="black" stroke-width="{2 if fret_idx == 1 else 1}"/>'
            )

        # Draw markers and number frets.
        for fret_idx, row in enumerate(self._cells):
            cx = -padding
            cy = int(padding + (fret_idx + 0.5) * fret_spacing)

            output.append(
                f'<text x="{cx}" y="{cy + 4}"'
                f' font-family="{font_family}" font-size="{font_size}"'
                f' text-anchor="middle"'
                f' transform="rotate({text_angle}, {cx}, {cy})">'
                f"{fret_idx}</text>"
            )

            for string_idx, cell in enumerate(row):
                if cell is not None:
                    cx = padding + string_idx * string_spacing
                    output.append(
                        f'<circle cx="{cx}" cy="{cy}" r="{circle_radius}"'
                        f' stroke="{cell.color}" fill="white"/>'
                    )
                    output.append(
                        f'<text x="{cx}" y="{cy + 4}" fill="{cell.color}"'
                        f' font-family="{font_family}" font-size="{font_size}"'
                        ' text-anchor="middle"'
                        f' transform="rotate({text_angle}, {cx}, {cy})">'
                        f"{cell.text}</text>"
                    )

        output += ["</g>", "</svg>"]
        return "\n".join(output) + "\n"

    def set(self, pos: tuple[int, int], value: Cell | None) -> None:
        self._cells[pos[0]][pos[1]] = value

    def walk(self) -> Iterator[tuple[tuple[int, int], int]]:
        for string_idx, string_note in enumerate(STRINGS):
            for fret in range(FRETS):
                yield (fret, string_idx), string_note + fret
