from typing import Dict, List

import numpy as np
import simpleaudio as sa

import scales

ALL_NOTES = scales.ALL_NOTES  # Dict that translates name of note to order in interval.
EVENT_DURATION = 0.25  # [seconds]: the time each note is played.
SAMPLE_RATE = 44100
REFERENCE_A = (
    440  # [Hz]: frequency of A4, which is a commonly used reference frequency.
)
REFERENCE_OCT = 4
LOWEST_OCTAVE = 3  # Here I set what the lowest octave to be played is.


def frequency_dict(octave: int) -> Dict[str, float]:
    """Generates a dictionary of frequencies for the notes in a given octave."""
    freq_dict = {}
    for note in ALL_NOTES:
        notes_from_ref_a = ALL_NOTES[note] + (octave - REFERENCE_OCT) * 12
        freq_dict[note] = REFERENCE_A * 2 ** (
            (notes_from_ref_a) / 12
        )  # Per definition, this equation returns the frequency of a note in a given interval.
    return freq_dict


def frequencies(scale: List[str]) -> List[float]:
    """Translates a scale to a list of frequencies."""

    frequencies = [0.0]
    octave_index = LOWEST_OCTAVE
    freq_index = 0
    for note in scale:
        freq = frequency_dict(octave_index)[note]
        if freq <= frequencies[freq_index]:
            octave_index += 1
            freq = frequency_dict(octave_index)[note]
        frequencies.append(freq)
        freq_index += 1

    frequencies = frequencies[1:]
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


def play_notes(note_array: np.ndarray):
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


# flow that funnels scale through the work:
def play_scale(scale: List[str], mode_number: int):
    freqs = frequencies(scale)
    notes = note_arrays(freqs)
    play_notes(notes)


def input_play_again(scale: List[str], mode_number: int):
    """Asks if the user wants to replay the scale."""
    valid_answers = [0, 1]
    while True:
        try:
            reply = int(
                input(
                    "Would you like to replay the scale?\n\tAnswer 1 to replay scale.\n\tAnswer 0 to restart program:\n\t"
                )
            )
        except ValueError:
            print(f"That's not a valid answer.")
            continue

        if reply == 1:
            play_scale(scale, mode_number)
        elif reply == 0:
            print("We're starting over!")
            break
        else:
            print("That is not a valid answer.")