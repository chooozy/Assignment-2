# NAME: Cameron Chen
# EMAIL: camerm3@uci.edu
# STUDENT ID: 49753193

''' Main Game Loop & Command Handling for Dr. Mario Inspired Game'''

from game_logic import Field

def run():
    rows = int(input())
    columns = int(input())
    game_config = str(input())

    field = Field(rows, columns)

    if game_config == 'CONTENTS':
        content_rows = []
        for _ in range(rows):
            content_rows.append(input())

        for r, row_contents in enumerate(content_rows):
            padded_row = row_contents.ljust(columns)
            for c in range(columns):
                char = padded_row[c]
                if char != ' ' and char.lower() in 'rby':
                    field.add_content(r, c, char)

        result = field.process_matches(get_command)
        if result == 'Q':
            return

    while True:
        field.print_field()  
        command = input().strip()

        if command == 'Q':
            break

        if command.startswith('F'):
            parts = command.split()
            if len(parts) >= 3:
                _, left, right = parts
                field.add_faller(left, right)

        elif command == 'A':
            if field.faller is not None and field.can_rotate():
                field.draw_faller()
                field.clear_faller()
                field.faller.rotate_clockwise()
                field.check_and_update_faller_state()

        elif command == 'B':
            if field.faller is not None and field.can_rotate():
                field.draw_faller()
                field.clear_faller()
                field.faller.rotate_counterclockwise()
                field.check_and_update_faller_state()
                
        elif command == '<':
            if field.faller is not None and field.can_move_left():
                field.draw_faller()
                field.clear_faller()
                field.faller.move_left()
                field.check_and_update_faller_state()

        elif command == '>':
            if field.faller is not None and field.can_move_right():
                field.draw_faller()
                field.clear_faller()
                field.faller.move_right()
                field.check_and_update_faller_state()

        elif command.startswith('V'):
            parts = command.split()
            if len(parts) == 4:
                _, row_str, col_str, color = parts
                row = int(row_str)
                col = int(col_str)
                field.add_virus(row, col, color)

        if command == '' or command == ' ':
            field.advance_time()
            if field.faller is None:
                result = field.process_matches(get_command)
                if result == 'Q':
                    break

        elif field.faller is not None and command != 'V':
            field.advance_time()
            if field.faller is None:
                result = field.process_matches(get_command)
                if result == 'Q':
                    break

def get_command():
    command = input().strip()
    return command

if __name__ == '__main__':
    run()
