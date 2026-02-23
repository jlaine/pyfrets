import unittest

from pyfrets.notes import (
    augment,
    diminish,
    note_name_to_pitch,
    prettify_chord,
    prettify_interval,
    prettify_note,
)


class NotesTest(unittest.TestCase):
    def test_augment(self) -> None:
        self.assertEqual(augment("C"), "C#")
        self.assertEqual(augment("Cb"), "C")

    def test_diminish(self) -> None:
        self.assertEqual(diminish("C"), "Cb")
        self.assertEqual(diminish("C#"), "C")

    def test_note_name_to_pitch(self) -> None:
        notes = {
            "C": 0,
            "C#": 1,
            "D": 2,
            "D#": 3,
            "E": 4,
            "F": 5,
            "G": 7,
            "G#": 8,
            "A": 9,
            "A#": 10,
            "B": 11,
        }
        key = "C"
        for name, pitch in notes.items():
            with self.subTest(name=name, key=key):
                self.assertEqual(note_name_to_pitch(name), pitch)

        with self.assertRaises(ValueError):
            note_name_to_pitch("X")

    def test_prettify_chord(self) -> None:
        notes = {
            "C": "C",
            "Cm": "Cm",
            "Cb": "C♭",
            "Cbm": "C♭m",
            "C#": "C♯",
            "Cdim": "C°",
        }
        for plain, pretty in notes.items():
            with self.subTest(plain=plain):
                self.assertEqual(prettify_chord(plain), pretty)

    def test_prettify_interval(self) -> None:
        intervals = {
            "1": "1",
            "b3": "♭3",
            "bb7": "𝄫7",
            "#5": "♯5",
        }
        for plain, pretty in intervals.items():
            with self.subTest(plain=plain):
                self.assertEqual(prettify_interval(plain), pretty)

    def test_prettify_note(self) -> None:
        notes = {
            "C": "C",
            "Cb": "C♭",
            "Cbb": "C𝄫",
            "C#": "C♯",
            "C##": "C𝄪",
        }
        for plain, pretty in notes.items():
            with self.subTest(plain=plain):
                self.assertEqual(prettify_note(plain), pretty)
