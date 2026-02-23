from typing import Sequence

NOTE_ALPHABET = ["C", "D", "E", "F", "G", "A", "B"]
NOTE_PITCHES = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

# Roman numerals.
ROMAN_NUMERALS_LOWER = ["i", "ii", "iii", "iv", "v", "vi", "vii"]
ROMAN_NUMERALS_UPPER = [num.upper() for num in ROMAN_NUMERALS_LOWER]
ROMAN_ALPHABET = ROMAN_NUMERALS_LOWER + ROMAN_NUMERALS_UPPER


def shift(root: int, pitches: Sequence[int]) -> list[int]:
    return [root + x for x in pitches]


def augment(note: str) -> str:
    """
    Augment the given note.
    """
    if note.endswith("b"):
        return note[:-1]
    else:
        return note + "#"


def diminish(note: str) -> str:
    """
    Diminish the given note.
    """
    if note.endswith("#"):
        return note[:-1]
    else:
        return note + "b"


def note_name_to_pitch(note: str) -> int:
    """
    Return the pitch to play the specified `note`.
    """
    try:
        pitch = NOTE_PITCHES[note[0]]
    except KeyError:
        raise ValueError("Unknown note %s" % note)
    for alteration in note[1:]:
        if alteration == "b":
            pitch -= 1
        else:
            pitch += 1
    return pitch % 12


def parse_note_alteration(note: str) -> tuple[str, str]:
    alteration = ""
    while note.endswith("#") or note.endswith("b"):
        alteration = note[-1] + alteration
        note = note[:-1]
    return note, alteration


def prettify_chord(chord: str) -> str:
    return prettify_note(chord).replace("dim", "°")


def prettify_interval(interval: str) -> str:
    return prettify_note(interval)


def prettify_note(note: str) -> str:
    return (
        note.replace("bb", "𝄫").replace("##", "𝄪").replace("b", "♭").replace("#", "♯")
    )
