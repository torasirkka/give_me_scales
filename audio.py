from typing import Dict, List
import re

import numpy as np
import simpleaudio as sa

import scales

# Dict that translates name of note to order in interval.
ALL_NOTES = scales.ALL_NOTES
EVENT_DURATION = 0.25  # [seconds]: the time each note is played.
SAMPLE_RATE = 44100
REFERENCE_A = (
    440  # [Hz]: frequency of A4, which is a commonly used reference frequency.
)
REFERENCE_OCT = 4
LOWEST_OCTAVE = 3  # Here I set what the lowest octave to be played is.


def frequency_dict(octave: int) -> Dict[str, float]:
    """Generates a dictionary of frequencies for all notes in a given octave."""
    freq_dict = {}
    for note in ALL_NOTES:
        notes_from_ref_a = ALL_NOTES[note] + (octave - REFERENCE_OCT) * 12
        freq_dict[note] = REFERENCE_A * 2 ** ((notes_from_ref_a) / 12)
    return freq_dict


def frequencies(scale: List[str]) -> List[float]:
    """Translates a scale to a list of frequencies.
    In order to make sure the right frequency of the note is played, I keep track of
    the last, the current frequency, and the current octave. A scale is a sequence of
    notes that increase in frequency. Hence, if the calculated note has lower frequency,
    it is time to go up a scale.
    A scale is typically played up and down, which is why the frequencies list is extended to
    include the frequencies 'backwards'."""
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


def timesteps(event_duration: float, sample_rate: float) -> np.ndarray:
    """Creates an array of discrete timesteps based on event duration (time[s]) and sample_rate [Hz]."""
    return np.linspace(0, event_duration, int(event_duration * sample_rate), False)


def wave_arrays(frequencies: List[float]) -> List[np.ndarray]:
    """Translates frequencies (floats) to discretized sine waves (arrays) corresponding to the notes."""
    discretized_time = timesteps(
        event_duration=EVENT_DURATION, sample_rate=SAMPLE_RATE)
    waves: List[np.ndarray] = []
    for f in frequencies:
        waves += [np.sin(f * 2 * np.pi * discretized_time)]

    return waves


def play_notes(wave_array: List[np.ndarray]):
    """A list of sinus wave arrays are played one after another.
    To accomplish this, the arrays are concatenated, converted to 16-bit data before being played
    by the sa module. The program waits for playback to finish before exiting."""
    audio = np.hstack((wave_array))
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    play_obj.wait_done()


def play_scale(scale: List[str], mode_number: int):
    """Support function that funnels a scale and mode number all the way to being played"""
    freqs = frequencies(scale)
    notes = wave_arrays(freqs)
    play_notes(notes)


def input_play_another_scale() -> str:
    """Asks if the user wants to hear another scale (for the same root note)."""
    return input(
        "Type a number between 1 and 7 to hear another scale or type 0 to start over with another root note. "
    )
