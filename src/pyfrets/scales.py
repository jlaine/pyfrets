import enum
import functools

from .notes import (
    NOTE_ALPHABET,
    augment,
    diminish,
    note_name_to_pitch,
    parse_note_alteration,
    prettify_note,
    shift,
)

ROMAN_NUMERALS_LOWER = ["i", "ii", "iii", "iv", "v", "vi", "vii"]


class Mode(enum.Enum):
    IONIAN = 1  # major scale
    DORIAN = 2
    PHRYGIAN = 3
    LYDIAN = 4
    MIXOLYDIAN = 5
    AEOLIAN = 6  # natural minor scale
    LOCRIAN = 7

    @property
    def pretty_name(self) -> str:
        return self.name.title()


def mode_chords(mode: Mode) -> list[str]:
    """
    Return the chords for the given diatonic mode.
    """
    offset = mode.value - 1
    qualities = ["M", "m", "m", "M", "M", "m", "dim"]
    output = []
    for pos, letter in enumerate(ROMAN_NUMERALS_LOWER):
        quality = qualities[(pos + offset) % 7]
        if quality == "M":
            output.append(letter.upper())
        elif quality == "m":
            output.append(letter)
        else:
            output.append(letter + "dim")
    return output


def mode_pitches(mode: Mode) -> list[int]:
    """
    Return the pitches for the given diatonic mode.
    """
    offset = mode.value - 1
    base = [2, 2, 1, 2, 2, 2, 1]
    output = [0]
    for step in base[offset:] + base[0:offset]:
        output.append(output[-1] + step)
    return output[:-1]


@functools.lru_cache
def scale_notes(root: str, mode: Mode) -> list[str]:
    """
    Return the notes for the given diatonic scale.
    """
    root_pitch = note_name_to_pitch(root)
    note_index = NOTE_ALPHABET.index(root[0])

    # Name notes in the key.
    note_names = [root]
    for offset in mode_pitches(mode)[1:]:
        note_index = (note_index + 1) % 7
        note_pitch = (root_pitch + offset) % 12

        # Find the accidental to match the pitch.
        note_letter = NOTE_ALPHABET[note_index]
        for note_name in [
            diminish(diminish(note_letter)),
            diminish(note_letter),
            note_letter,
            augment(note_letter),
            augment(augment(note_letter)),
        ]:
            if note_name_to_pitch(note_name) == note_pitch:
                note_names.append(note_name)
                break
        else:
            raise ValueError(
                f"{root} {mode.pretty_name} scale requires too many accidentals"
            )

    return note_names


class Scale:
    def __init__(self, root: str, mode: Mode) -> None:
        self._mode = mode
        self._root = root

    @property
    def mode(self) -> Mode:
        return self._mode

    @property
    def notes(self) -> list[str]:
        """
        The names of the notes making up the scale.
        """
        return scale_notes(self._root, self._mode)

    @property
    def pitches(self) -> list[int]:
        """
        The pitches of the notes making up the scale.
        """
        root_pitch = note_name_to_pitch(self._root)
        return shift(root_pitch, mode_pitches(self._mode))

    @property
    def pretty_name(self) -> str:
        """
        The pretty name of the scale.
        """
        return f"{prettify_note(self._root)} {self._mode.pretty_name}"

    @property
    def pretty_notes(self) -> list[str]:
        """
        The pretty names of the notes making up the scale.
        """
        return [prettify_note(note) for note in self.notes]

    @property
    def pretty_root(self) -> str:
        """
        The pretty name of the root note of the scale.
        """
        return prettify_note(self._root)

    @property
    def roman_chords(self) -> list[str]:
        return mode_chords(self.mode)

    @property
    def root(self) -> str:
        """
        The name of the root note of the scale.
        """
        return self._root

    def note_from_roman(self, roman: str) -> str:
        """
        Return the note name for the given `roman` numeral.
        """
        numeral, alteration = parse_note_alteration(roman)
        index = ROMAN_NUMERALS_LOWER.index(numeral.lower())
        return self.notes[index] + alteration
