from typing import Dict, List

SHARP_NOTES = [
    "A",
    "A#",
    "B",
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
]
FLAT_NOTES = [
    "A",
    "Bb",
    "B",
    "C",
    "Db",
    "D",
    "Eb",
    "E",
    "F",
    "Gb",
    "G",
    "Ab",
    "A",
    "Bb",
    "B",
    "C",
    "Db",
    "D",
    "Eb",
    "E",
    "F",
    "Gb",
    "G",
    "G#",
]

EQUIVALENT_NOTES = {"Fb": "E", "E#": "F", "B#": "C", "Cb": "B"}

ALL_NOTES = {
    "A": 0,
    "A#": 1,
    "Bb": 1,
    "B": 2,
    "Cb": 2,
    "B#": 3,
    "C": 3,
    "C#": 4,
    "Db": 4,
    "D": 5,
    "D#": 6,
    "Eb": 6,
    "E": 7,
    "Fb": 7,
    "E#": 8,
    "F": 8,
    "F#": 9,
    "Gb": 9,
    "G": 10,
    "G#": 11,
    "Ab": 11,
}

SHARP_ROOT_NOTES = ["C", "G", "D", "A", "E", "B", "F#"]

SCALES_AND_MODES = {
    1: "Ioanian/ Major",
    2: "Dorian",
    3: "Phrygian",
    4: "Lydian",
    5: "Mixolydian",
    6: "Aeolian/ Natural minor",
    7: "Locrian",
}

MODE_PATTERNS = {
    1: [0, 2, 4, 5, 7, 9, 11, 12],
    2: [0, 2, 3, 5, 7, 9, 10, 12],
    3: [0, 1, 3, 5, 7, 8, 10, 12],
    4: [0, 2, 4, 6, 7, 9, 11, 12],
    5: [0, 2, 4, 5, 7, 9, 10, 12],
    6: [0, 2, 3, 5, 7, 8, 10, 12],
    7: [0, 1, 3, 5, 6, 8, 10, 12],
}


def print_greeting():
    """Prints greeting and purpose of this program."""
    print(
        "\nHi there! \nI can help you figure out the notes of a scale or mode of your choice!\n"
    )


def input_valid_root_note() -> str:
    """Asks user for a root note until a valid one is given."""
    while True:
        root_note = (
            input("What root note do you want to work with? ").strip().capitalize()
        )
        if root_note in EQUIVALENT_NOTES:
            print(
                f"\n\tAlright, {root_note}! I'll call this note {EQUIVALENT_NOTES[root_note]}, which is just another way to reference that note.\n"
            )
            return EQUIVALENT_NOTES[root_note]

        if root_note in ALL_NOTES:
            print(f"\n\tGreat, {root_note} it is!\n")
            return root_note

        else:
            print(
                f"\n\tThat's not a note I am familiar with. The notes you currently can choose from are: \n\t{', '.join(x for x in ALL_NOTES.keys())}.\n"
            )


def input_valid_scale() -> int:
    """Asks user for a scale until a valid one is given."""
    while True:
        print("\tHere are the scales I currently am aware of:")
        for key, value in SCALES_AND_MODES.items():
            print(f"\t{value} ({key})")
        print("")

        try:
            scale_number = int(
                input("What's the number of the scale or mode you seek? ")
            )

        except ValueError:
            print("\nUm, that's not a number. How about we try that again?\n")
            continue

        if scale_number in SCALES_AND_MODES:
            return scale_number
        else:
            print(
                "\nUups! That number does not map to any of my scales or modes. Let's try again.\n"
            )


def mode_pattern(mode_number: int) -> List[int]:
    """Translates mode number to a pattern of offsets (relative to the root note)."""
    return MODE_PATTERNS[mode_number]


def scale(root_note: str, mode_number: int) -> List[str]:
    """Builds a notes list (scale) based on the root note and mode number."""
    if sharp_mode(root_note) == True:
        notes = SHARP_NOTES
    else:
        notes = FLAT_NOTES

    pattern = mode_pattern(mode_number)
    root_note_index = ALL_NOTES[root_note]
    scale = []

    for offset in pattern:
        scale.append(notes[root_note_index + offset])

    return scale


def sharp_mode(root_note: str) -> bool:
    """Checks if the root note is sharp."""
    is_sharp = root_note in SHARP_ROOT_NOTES
    return is_sharp


def print_scale(root_note: str, mode_number: int, scale: List[str]):
    """Prints the name, root note and notes in the scale."""
    mode_name = SCALES_AND_MODES[mode_number]
    print(f"\n\tThe {root_note} {mode_name} scale contains the following notes:")
    print(f"\t{', '.join(x for x in scale)}\n")