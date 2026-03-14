import argparse
import dataclasses
import re
from fractions import Fraction
from typing import Iterable

import mido

from pyfrets.chords import Chord
from pyfrets.notes import prettify_chord
from pyfrets.scales import Mode, Scale
from pyfrets.tracks import Track


@dataclasses.dataclass
class Song:
    chord_pattern: str
    key: str
    beats_per_minute: int = 120
    strum_pattern: str = "D-D-D-D-"

    @property
    def scale(self) -> Scale:
        m = re.match("^([A-G]) (major|minor)$", self.key)
        assert m, "Could not parse key"
        if m.group(2) == "major":
            return Scale(m.group(1), Mode.IONIAN)
        else:
            return Scale(m.group(1), Mode.AEOLIAN)


SONGS = {
    "50s": Song(
        chord_pattern="I vi IV V",
        key="C major",
    ),
    "50-ways-to-leave-your-lover": Song(
        chord_pattern="i/III VII6 VImaj7 V7b9 "
        + "i VII#dim7 IIdim7 Vaug7 "
        + "i VII6 VImaj7 V7b9 "
        + "i iv7 i",
        key="E minor",
        strum_pattern="D---",
    ),
    "blues": Song(
        chord_pattern="I7 I7 I7 I7 IV7 IV7 I7 I7 V7 IV7 I7 V7",
        key="A minor",
    ),
    "blues-quick-change": Song(
        chord_pattern="I7 IV7 I7 I7 IV7 IV7 I7 I7 V7 IV7 I7 V7",
        key="A minor",
    ),
    "blues-slow-change": Song(
        chord_pattern="I7 I7 I7 I7 IV7 IV7 I7 I7 V7 V7 I7 I7",
        key="A minor",
    ),
    "blues7": Song(
        chord_pattern="I IV I I7 IV IV7 I I7 V IV I V7",
        key="A minor",
        strum_pattern="D-DU-UD-/D-DU-UDU",
    ),
    "for-you-blue": Song(
        beats_per_minute=90,
        chord_pattern="I7 IV7 I7 I7 IV7 IV7 I7 I7 V7 IV7 I7 V7",
        key="D minor",
    ),
    "hey-jude": Song(
        beats_per_minute=150,
        chord_pattern=(
            "I I V V V7 V7 I I IV IV I I V V7 I I "  # verse
            + "I7 I7 IV IVmaj7/iii ii7 IV/I V7 V7 I I"  # chorus
        ),
        key="F major",
        strum_pattern="D-D-D-DU",
    ),
    "key": Song(
        chord_pattern="I ii iii IV V vi viidim",
        key="A major",
    ),
    "paint-it-black": Song(
        beats_per_minute=160,
        chord_pattern="i VII III VII i i i i i VII III VII IV IV V/iv V/iv",
        key="E minor",
        strum_pattern="D-DU/DUD/U-UD/U-UD-",
    ),
    "pop": Song(
        chord_pattern="I V vi IV",
        key="C major",
    ),
}


def print_scale_chords(scale: Scale, romans: Iterable[str]) -> None:
    print("== %s ==" % scale.pretty_name)
    for chord_roman in romans:
        chord = Chord.from_roman(chord_roman, scale)
        print(
            "%-6s %-6s : %s"
            % (
                prettify_chord(chord_roman),
                chord.pretty_name,
                " ".join(["%-2s" % note for note in chord.pretty_notes]),
            )
        )
    print()


def print_song_info(song: Song) -> None:
    chord_pattern_roman = song.chord_pattern.split()
    chord_pattern = [Chord.from_roman(c, song.scale) for c in chord_pattern_roman]

    # Print chord pattern.
    print_scale_chords(song.scale, set(chord_pattern_roman))
    print("== chord pattern ==")
    print(" ".join("%-6s" % prettify_chord(x) for x in chord_pattern_roman))
    print(" ".join("%-6s" % chord.pretty_name for chord in chord_pattern))
    print()

    # Print strumming pattern.
    print("== strumming pattern ==")
    print(song.strum_pattern)
    print()


def strum_song(*, repeat: int, song: Song) -> Track:
    track = Track(beats_per_minute=song.beats_per_minute)

    chord_pattern_roman = song.chord_pattern.split()
    chord_pattern = [Chord.from_roman(c, song.scale) for c in chord_pattern_roman]

    half_beat = Fraction(1, 2)
    strum_events: list[list[Fraction]] = []
    for chunk in song.strum_pattern.split("/"):
        events = []
        assert chunk[0] in ("D", "U"), "strum pattern chunk must start with a strum"
        for strum in chunk:
            if strum in ("D", "U"):
                events.append(half_beat)
            else:
                assert strum == "-"
                events[-1] += half_beat
        strum_events.append(events)

    strum_index = 0
    for _ in range(repeat):
        for chord in chord_pattern:
            pitches = [p + 48 for p in chord.pitches]
            for duration in strum_events[strum_index]:
                track.add_notes(duration=duration, pitches=pitches)
            strum_index = (strum_index + 1) % len(strum_events)

    return track


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play with notes")

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="The command to run."
    )

    subparser = subparsers.add_parser("chords")
    subparser.add_argument("--minor", action="store_true")
    subparser.add_argument(
        "--scale-mode", default=Mode.IONIAN, type=lambda x: Mode(int(x))
    )
    subparser.add_argument("--scale-root", default="C")

    subparser = subparsers.add_parser("notes")
    subparser.add_argument(
        "--scale-mode", default=Mode.IONIAN, type=lambda x: Mode(int(x))
    )
    subparser.add_argument("--scale-root", default="C")

    subparser = subparsers.add_parser("render")
    subparser.add_argument("--repeat", type=int, default=1)
    subparser.add_argument("--song", type=str, choices=SONGS.keys(), required=True)

    options = parser.parse_args()

    if options.command == "chords":
        scale = Scale(options.scale_root, options.scale_mode)
        print_scale_chords(scale, scale.roman_chords)
    elif options.command == "notes":
        scale = Scale(options.scale_root, options.scale_mode)
        print(
            "%s : %s"
            % (
                scale.pretty_name,
                " ".join(["%-2s" % note for note in scale.pretty_notes]),
            )
        )
    else:
        song = SONGS[options.song]
        print_song_info(song)
        track = strum_song(repeat=options.repeat, song=song)

        # Save to MIDI file.
        mid_file = mido.MidiFile()
        mid_file.tracks.append(track.to_midi())
        mid_file.save(options.song + ".mid")
