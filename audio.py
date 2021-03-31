import numpy as np
import simpleaudio as sa
import scales
from typing import Dict, List

ALL_NOTES = scales.ALL_NOTES
EVENT_DURATION = 0.25  # [seconds]: the time each note is played.
SAMPLE_RATE = 44100
LOWEST_A = 220  # [Hz]: frequency of A3, which is chosen to be the reference frequency, meaning it is the lowest note to be played.

# Calculate frequencies and store them in two dicts for two intervals. This is
# needed to play scales that smoothly increases or decreases.

FREQUENCY_DICT = {}
FREQUENCY_DICT_NEXT_OCTAVE = {}
for note in ALL_NOTES:
    frequency = LOWEST_A * 2 ** (ALL_NOTES[note] / 12)
    FREQUENCY_DICT[note] = frequency
    FREQUENCY_DICT_NEXT_OCTAVE[note] = 2 * frequency


def slice_index(scale: List[str]) -> int:
    slice_index = 0
    previous_note_index = 0
    for note in scale:
        note_index = ALL_NOTES[note]
        if note_index < previous_note_index:
            slice_index = scale.index(note)
        previous_note_index = note_index
    return slice_index


def frequencies(scale: List[str], slice_index) -> List[float]:
    """Translates a scale to a list of frequencies."""
    notes_1st_octaves = scale[:slice_index]
    notes_2st_octaves = scale[slice_index:]

    frequencies = []
    for note in notes_1st_octaves:
        frequencies.append(FREQUENCY_DICT[note])
    for note in notes_2st_octaves:
        frequencies.append(FREQUENCY_DICT_NEXT_OCTAVE[note])

    backwards = frequencies[::-1]
    frequencies = frequencies + backwards[1:]
    return frequencies


# get timesteps for each sample, T is note duration in seconds
def timesteps(event_duration: float, sample_rate: float) -> np.ndarray:
    """Creates an array of discrete timesteps."""

    return np.linspace(0, event_duration, int(event_duration * sample_rate), False)


def note_arrays(frequencies: List[float]) -> List[np.ndarray]:
    """Generate sine wave notes."""
    steps = timesteps(event_duration=EVENT_DURATION, sample_rate=SAMPLE_RATE)
    notes: List[np.ndarray] = []
    for f in frequencies:
        notes += [np.sin(f * 2 * np.pi * steps)]
    return notes


def play_notes(note_array):
    """plays a note"""
    # concatenate notes
    audio = np.hstack((note_array))
    # normalize to 16-bit range
    audio *= 32767 / np.max(np.abs(audio))
    # convert to 16-bit data
    audio = audio.astype(np.int16)
    # start playback
    play_obj = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    # wait for playback to finish before exiting
    play_obj.wait_done()