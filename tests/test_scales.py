import unittest

from pyfrets.scales import Mode, Scale


class ScalesTest(unittest.TestCase):
    def test_major_notes(self) -> None:
        # Valid scales.
        scales = {
            # Usual scales.
            "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
            "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
            "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
            "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
            "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
            "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
            "F": ["F", "G", "A", "Bb", "C", "D", "E"],
            "C": ["C", "D", "E", "F", "G", "A", "B"],
            "G": ["G", "A", "B", "C", "D", "E", "F#"],
            "D": ["D", "E", "F#", "G", "A", "B", "C#"],
            "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
            "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
            "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
            "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
            "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
            # Theoretical scales.
            "A#": ["A#", "B#", "C##", "D#", "E#", "F##", "G##"],
            "B#": ["B#", "C##", "D##", "E#", "F##", "G##", "A##"],
            "D#": ["D#", "E#", "F##", "G#", "A#", "B#", "C##"],
            "E#": ["E#", "F##", "G##", "A#", "B#", "C##", "D##"],
            "Fb": ["Fb", "Gb", "Ab", "Bbb", "Cb", "Db", "Eb"],
            "G#": ["G#", "A#", "B#", "C#", "D#", "E#", "F##"],
        }
        for root, notes in scales.items():
            with self.subTest(root=root):
                scale = Scale(root, Mode.IONIAN)
                self.assertEqual(scale.notes, notes)

        # Invalid scales.
        for root in [
            "A##",
            "B##",
            "D##",
            "E##",
            "Fbb",
            "G##",
        ]:
            with self.subTest(root=root):
                scale = Scale(root, Mode.IONIAN)
                with self.assertRaises(ValueError) as cm:
                    print(scale.notes)
                self.assertEqual(
                    str(cm.exception),
                    f"{root} Ionian scale requires too many accidentals",
                )

    def test_major_properties(self) -> None:
        scale = Scale("Cb", Mode.IONIAN)
        self.assertEqual(scale.mode, Mode.IONIAN)
        self.assertEqual(scale.pitches, [11, 13, 15, 16, 18, 20, 22])
        self.assertEqual(scale.root, "Cb")
        self.assertEqual(scale.pretty_name, "C♭ Ionian")
        self.assertEqual(scale.pretty_notes, ["C♭", "D♭", "E♭", "F♭", "G♭", "A♭", "B♭"])
        self.assertEqual(scale.pretty_root, "C♭")

    def test_minor_notes(self) -> None:
        # Valid scales.
        scales = {
            # Usual scales.
            "Eb": ["Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"],
            "Bb": ["Bb", "C", "Db", "Eb", "F", "Gb", "Ab"],
            "F": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
            "C": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
            "G": ["G", "A", "Bb", "C", "D", "Eb", "F"],
            "D": ["D", "E", "F", "G", "A", "Bb", "C"],
            "A": ["A", "B", "C", "D", "E", "F", "G"],
            "E": ["E", "F#", "G", "A", "B", "C", "D"],
            "B": ["B", "C#", "D", "E", "F#", "G", "A"],
            "F#": ["F#", "G#", "A", "B", "C#", "D", "E"],
            "C#": ["C#", "D#", "E", "F#", "G#", "A", "B"],
            "G#": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
            "D#": ["D#", "E#", "F#", "G#", "A#", "B", "C#"],
            # Theoretical scales.
            "B#": ["B#", "C##", "D#", "E#", "F##", "G#", "A#"],
            "Cb": ["Cb", "Db", "Ebb", "Fb", "Gb", "Abb", "Bbb"],
            "Db": ["Db", "Eb", "Fb", "Gb", "Ab", "Bbb", "Cb"],
            "E#": ["E#", "F##", "G#", "A#", "B#", "C#", "D#"],
            "Fb": ["Fb", "Gb", "Abb", "Bbb", "Cb", "Dbb", "Ebb"],
            "Gb": ["Gb", "Ab", "Bbb", "Cb", "Db", "Ebb", "Fb"],
        }
        for root, notes in scales.items():
            with self.subTest(root=root):
                scale = Scale(root, Mode.AEOLIAN)
                self.assertEqual(scale.notes, notes)

        # Invalid scales.
        for root in [
            "B##",
            "Cbb",
            "Dbb",
            "E##",
            "Fbb",
            "Gbb",
        ]:
            with self.subTest(root=root):
                scale = Scale(root, Mode.AEOLIAN)
                with self.assertRaises(ValueError) as cm:
                    scale.notes
                self.assertEqual(
                    str(cm.exception),
                    f"{root} Aeolian scale requires too many accidentals",
                )

    def test_minor_properties(self) -> None:
        scale = Scale("Cb", Mode.AEOLIAN)
        self.assertEqual(scale.mode, Mode.AEOLIAN)
        self.assertEqual(scale.pitches, [11, 13, 14, 16, 18, 19, 21])
        self.assertEqual(scale.root, "Cb")
        self.assertEqual(scale.pretty_name, "C♭ Aeolian")
        self.assertEqual(scale.pretty_notes, ["C♭", "D♭", "E𝄫", "F♭", "G♭", "A𝄫", "B𝄫"])
        self.assertEqual(scale.pretty_root, "C♭")

    def test_note_from_roman(self) -> None:
        notes = {
            "I": "C",
            "II": "D",
            "III": "E",
            "IV": "F",
            "V": "G",
            "VI": "A",
            "VII": "B",
            "VII#": "B#",
            "VIIbb": "Bbb",
        }
        scale = Scale("C", Mode.IONIAN)
        for roman, name in notes.items():
            with self.subTest(roman=roman, scale=scale):
                self.assertEqual(scale.note_from_roman(roman), name)

    def test_roman_chords(self) -> None:
        scale = Scale("C", Mode.IONIAN)
        self.assertEqual(
            scale.roman_chords, ["I", "ii", "iii", "IV", "V", "vi", "viidim"]
        )

        scale = Scale("C", Mode.AEOLIAN)
        self.assertEqual(
            scale.roman_chords, ["i", "iidim", "III", "iv", "v", "VI", "VII"]
        )
