import argparse
import sys
import typing

from pyfrets.chords import Chord
from pyfrets.guitar import Cell, Fretboard, Orientation
from pyfrets.scales import Mode, Scale

SCALE_NOTE_COLORS = ["red", "black", "green", "magenta", "blue", "black", "magenta"]
SCALE_NOTE_FUNCTIONS = ["R", "2", "3", "4", "5", "6", "7"]

T = typing.TypeVar("T")


def pentatonic(lst: list[T]) -> list[T]:
    return [lst[x] for x in [0, 2, 3, 4, 6]]


def plot_notes(
    *,
    basename: str,
    note_colors: list[str],
    note_texts: list[str],
    note_values: list[int],
    orientation: Orientation,
) -> None:
    # Place notes on fretboard.
    board = Fretboard()
    note_values = [i % 12 for i in note_values]
    for pos, note_value in board.walk():
        try:
            idx = note_values.index(note_value % 12)
        except ValueError:
            continue
        board.set(pos, Cell(color=note_colors[idx], text=note_texts[idx]))

    # Display fretboard.
    sys.stdout.write(board.dump_ansi(orientation=orientation))

    # Write files.
    with open(basename + ".svg", "w") as fp:
        fp.write(board.dump_svg(orientation=orientation))


def main() -> None:
    parser = argparse.ArgumentParser(description="Display notes on a guitar")
    parser.add_argument(
        "--note-names",
        action="store_true",
        help="Show note names instead of their function.",
    )
    parser.add_argument(
        "--portrait",
        action="store_true",
        help="Show the fretboard in portrait mode.",
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="The command to run."
    )
    subparser = subparsers.add_parser("scale", help="Show the notes of a scale.")
    subparser.add_argument("--pentatonic", action="store_true")
    subparser.add_argument(
        "--scale-mode", default=Mode.IONIAN, type=lambda x: Mode(int(x))
    )
    subparser.add_argument("--scale-root", default="C")

    subparser = subparsers.add_parser("chord", help="Show the notes of a chord.")
    subparser.add_argument("chord")
    options = parser.parse_args()

    if options.portrait:
        orientation = Orientation.PORTRAIT
    else:
        orientation = Orientation.LANDSCAPE

    # Determine notes.
    if options.command == "scale":
        scale = Scale(options.scale_root, options.scale_mode)
        note_colors = SCALE_NOTE_COLORS
        note_functions = SCALE_NOTE_FUNCTIONS
        note_names = scale.pretty_notes
        note_values = scale.pitches

        if options.pentatonic:
            note_colors = pentatonic(note_colors)
            note_functions = pentatonic(note_functions)
            note_names = pentatonic(note_names)
            note_values = pentatonic(note_values)

        # Display note names.
        for function, name in zip(note_functions, note_names):
            sys.stdout.write(f"{function} = {name}\n")

        plot_notes(
            basename=f"scale-{options.scale_root}-mode-{options.scale_mode.name.lower()}",
            note_colors=note_colors,
            note_texts=note_names if options.note_names else note_functions,
            note_values=note_values,
            orientation=orientation,
        )

    else:
        chord = Chord(options.chord)
        note_functions = chord.quality.pretty_intervals
        note_names = chord.pretty_notes
        note_values = chord.pitches

        # Display note names.
        for function, name in zip(note_functions, note_names):
            sys.stdout.write(f"{function:3} = {name}\n")

        plot_notes(
            basename=f"chord-{options.chord}",
            note_colors=[SCALE_NOTE_COLORS[i] for i in range(len(note_values))],
            note_texts=note_names if options.note_names else note_functions,
            note_values=note_values,
            orientation=orientation,
        )


if __name__ == "__main__":
    main()
