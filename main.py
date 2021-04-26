import scales
import audio
import enum


class States(enum.Enum):
    GET_ROOT_NOTE = 1
    PRINT_SCALE_TO_NUMBER_MAPPING = 2
    GET_SCALE = 3
    PRINT_SCALES = 4
    PLAY_NOTES = 5
    ASK_FOR_ANOTHER_SCALE = 6


def main():
    """Function that loops user through the program cycle: asking for scale name and root note, returning the scale."""

    scales.print_greeting()
    state = States.GET_ROOT_NOTE
    while True:
        if state == States.GET_ROOT_NOTE:
            root_note = scales.input_valid_root_note()
            state = States.PRINT_SCALE_TO_NUMBER_MAPPING

        elif state == States.PRINT_SCALE_TO_NUMBER_MAPPING:
            scales.print_scale_to_number_mapping()
            state = States.GET_SCALE

        elif state == States.GET_SCALE:
            response = scales.input_scale()
            if scales.valid_number(response, valid_answers=list(scales.SCALES_AND_MODES.keys())):
                mode_number = int(response)
                scale = scales.scale(root_note, mode_number)
                state = States.PRINT_SCALES

        elif state == States.PRINT_SCALES:
            scales.print_scale(root_note, mode_number, scale)
            state = States.PLAY_NOTES

        elif state == States.PLAY_NOTES:
            audio.play_scale(scale, mode_number)
            state = States.ASK_FOR_ANOTHER_SCALE

        elif state == States.ASK_FOR_ANOTHER_SCALE:
            response = audio.input_play_another_scale()
            if scales.valid_number(response, valid_answers=(list(scales.SCALES_AND_MODES) + [0])):
                if int(response) == 0:
                    state = States.GET_ROOT_NOTE
                else:
                    mode_number = int(response)
                    scale = scales.scale(root_note, mode_number)
                    state = States.PRINT_SCALES


if __name__ == "__main__":
    main()
