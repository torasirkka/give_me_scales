import code as c


def main():
    """Function that loops user through the program cycle: asking for scale name and root note, returning the scale."""
    c.print_greeting()
    while True:
        root_note = c.input_valid_root_note()
        mode_number = c.input_valid_scale()
        scale = c.scale(root_note, mode_number)
        c.print_scale(root_note, mode_number, scale)


if __name__ == "__main__":
    main()