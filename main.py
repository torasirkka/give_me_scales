import scales
import audio


def main():
    """Function that loops user through the program cycle: asking for scale name and root note, returning the scale."""

    scales.print_greeting()
    while True:
        root_note = scales.input_valid_root_note()
        mode_number = scales.input_valid_scale()
        scale = scales.scale(root_note, mode_number)
        scales.print_scale(root_note, mode_number, scale)

        audio.play_scale(scale, mode_number)
        audio.play_again_execution(scale, mode_number)


if __name__ == "__main__":
    main()