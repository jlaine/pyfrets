import dataclasses
import functools
import re

from .notes import (
    NOTE_ALPHABET,
    ROMAN_ALPHABET,
    augment,
    diminish,
    note_name_to_pitch,
    parse_note_alteration,
    prettify_chord,
    prettify_interval,
    prettify_note,
    shift,
)
from .scales import Mode, Scale

MAJOR_SCALE = (0, 2, 4, 5, 7, 9, 11)


@dataclasses.dataclass(frozen=True)
class Quality:
    """
    A chord quality made up of two or more intervals.
    """

    name: str
    "The name of the quality."

    intervals: tuple[str, ...]
    "The names of the intervals that make up the quality."

    description: str
    "A textual description of the quality."

    @functools.cached_property
    def pitches(self) -> list[int]:
        """
        The pitch offset of the intervals that make up the quality.
        """
        return [_get_interval_pitch(i) for i in self.intervals]

    @property
    def pretty_intervals(self) -> list[str]:
        """
        The pretty names of the intervals that make up the quality.
        """
        return [prettify_interval(i) for i in self.intervals]


CHORD_QUALITIES = {
    quality.name: quality
    for quality in [
        # 3 notes
        Quality("", ("1", "3", "5"), "major triad"),
        Quality("m", ("1", "b3", "5"), "minor triad"),
        Quality("aug", ("1", "3", "#5"), "augmented triad"),
        Quality("dim", ("1", "b3", "b5"), "diminished triad"),
        Quality("sus2", ("1", "2", "5"), "suspended second"),
        Quality("sus4", ("1", "4", "5"), "suspended fourth"),
        # 4 notes
        Quality("6", ("1", "3", "5", "6"), "major sixth"),
        Quality("m6", ("1", "b3", "5", "6"), "minor sixth"),
        Quality("7", ("1", "3", "5", "b7"), "dominant seventh"),
        Quality("7b5", ("1", "3", "b5", "b7"), "dominant seventh flat five"),
        Quality("maj7", ("1", "3", "5", "7"), "major seventh"),
        Quality("m7", ("1", "b3", "5", "b7"), "minor seventh"),
        Quality("m7b5", ("1", "b3", "b5", "b7"), "minor seventh flat five"),
        Quality("mmaj7", ("1", "b3", "5", "7"), "minor major seventh"),
        Quality("aug7", ("1", "3", "#5", "b7"), "augmented seventh"),
        Quality("augmaj7", ("1", "3", "#5", "7"), "augmented major seventh"),
        Quality("dim7", ("1", "b3", "b5", "bb7"), "diminished seventh"),
        Quality("dimmaj7", ("1", "b3", "b5", "7"), "diminished major seventh"),
        Quality("add4", ("1", "3", "4", "5"), "major add fourth"),
        Quality("madd4", ("1", "b3", "4", "5"), "minor add fourth"),
        Quality("add9", ("1", "3", "4", "9"), "major add ninth"),
        Quality("madd9", ("1", "b3", "4", "9"), "minor add ninth"),
        # 5 notes
        Quality("9", ("1", "3", "5", "b7", "9"), "dominant ninth"),
        Quality("maj9", ("1", "3", "5", "7", "9"), "major ninth"),
        Quality("m9", ("1", "b3", "5", "b7", "9"), "minor ninth"),
        Quality("7b9", ("1", "3", "5", "b7", "b9"), "dominant seventh flat nine"),
        # 6 notes
        Quality("11", ("1", "3", "5", "b7", "9", "11"), "dominant eleventh"),
        Quality("7#11", ("1", "3", "5", "b7", "9", "#11"), "dominant sharp eleventh"),
        Quality("maj11", ("1", "3", "5", "7", "9", "11"), "major eleventh"),
        Quality("m11", ("1", "b3", "5", "b7", "9", "11"), "minor eleventh"),
    ]
}


def _apply_interval_to_note(root: str, interval: str) -> str:
    alterations, offset = _parse_interval(interval)

    # Apply the interval and alteration.
    notes_in_key = Scale(root, Mode.IONIAN).notes
    note = notes_in_key[offset % 7]
    for alteration in alterations:
        if alteration == "#":
            note = augment(note)
        else:
            note = diminish(note)
    return note


def _get_interval_pitch(interval: str) -> int:
    alterations, offset = _parse_interval(interval)

    value = MAJOR_SCALE[offset % 7] + 12 * (offset // 7)
    for alteration in alterations:
        if alteration == "#":
            value += 1
        else:
            value -= 1
    return value


def _parse_interval(interval: str) -> tuple[str, int]:
    m = re.match(r"^([b#]*)(\d+)$", interval)
    assert m, f"Invalid interval {interval}"
    alterations = m.group(1)
    offset = int(m.group(2)) - 1
    return alterations, offset


def _parse_chord_name(name: str, alphabet: list[str]) -> tuple[str, Quality, str]:
    alphabet_re = "(?:" + ("|".join(alphabet)) + ")[b#]?"
    quality_re = "|".join(CHORD_QUALITIES.keys())
    chord_re = re.compile(
        "^(" + alphabet_re + ")(" + quality_re + ")(?:/(" + alphabet_re + "))?$"
    )
    m = chord_re.match(name)
    if not m:
        raise ValueError("Could not parse chord notation %s" % name)
    root = m.group(1)
    quality = CHORD_QUALITIES[m.group(2)]
    over = m.group(3)
    return root, quality, over


class Chord:
    """
    A chord made up of two or more notes.
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self._root, self._quality, self._over = _parse_chord_name(name, NOTE_ALPHABET)

    @property
    def description(self) -> str:
        """
        A textual description of the chord.
        """
        description = f"{self.root} {self.quality.description}"
        if self._over:
            description += f" over {self._over}"
        return description

    @property
    def name(self) -> str:
        """
        The name of the chord.
        """
        return self._name

    @property
    def notes(self) -> list[str]:
        """
        The names of the notes making up the chord.
        """
        notes = [
            _apply_interval_to_note(self._root, interval)
            for interval in self._quality.intervals
        ]
        if self._over:
            notes.insert(0, self._over)
        return notes

    @property
    def pitches(self) -> list[int]:
        """
        The pitches of the notes making up the chord.
        """
        root_pitch = note_name_to_pitch(self._root)

        pitches = shift(root_pitch, self._quality.pitches)
        if self._over:
            over_pitch = note_name_to_pitch(self._over)
            if over_pitch >= root_pitch:
                over_pitch -= 12
            pitches.insert(0, over_pitch)

        return pitches

    @property
    def pretty_name(self) -> str:
        """
        The pretty name of the chord.
        """
        return prettify_chord(self._name)

    @property
    def pretty_notes(self) -> list[str]:
        """
        The pretty names of the notes making up the chord.
        """
        return [prettify_note(n) for n in self.notes]

    @property
    def pretty_root(self) -> str:
        """
        The pretty name of the root note of the chord.
        """
        return prettify_note(self._root)

    @property
    def quality(self) -> Quality:
        """
        The quality of the chord.
        """
        return self._quality

    @property
    def root(self) -> str:
        """
        The name of the root note of the chord.
        """
        return self._root

    @classmethod
    def from_roman(cls, roman: str, scale: Scale) -> "Chord":
        """
        Return a chord for the given `roman` chord notation in the specified `scale`.
        """
        numeral, quality, over = _parse_chord_name(roman, ROMAN_ALPHABET)
        numeral, alteration = parse_note_alteration(numeral)

        # get root
        minor = numeral.islower()
        chord = scale.note_from_roman(numeral) + alteration
        if minor and quality.name != "dim":
            chord += "m"
        chord += quality.name

        # bass
        if over:
            chord += "/" + scale.note_from_roman(over)

        return cls(chord)
