import code as c

c.print_greeting()


def main():

    while True:
        root_note = c.input_valid_root_note()
        mode_number = c.input_valid_scale()
        scale = c.scale(root_note, mode_number)
        c.print_scale(root_note, mode_number, scale)


if __name__ == "__main__":
    main()