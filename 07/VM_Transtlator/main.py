from code_writer import CodeWriter
from vm_parser import Parser
import sys


def main():
    # initialize variables and objects
    root = f"C:\\Users\\User\\coding\\nand2tetris\\projects\\07\\{sys.argv[1]}\\{sys.argv[-1]}"
    name = root.split('\\')[-1]
    input_dir = f'{root}\\{name}.vm'
    output_dir = f'{root}\\{name}.asm'
    parser = Parser(input_dir)
    code_writer = CodeWriter(output_dir)

    while parser.has_more_lines_advance():
        if not parser.is_command():
            continue

        command = parser.current_command.split()[0]
        arg1 = parser.arg1()
        if parser.command_type() == Parser.C_ARITHMETIC:
            code_writer.write_arithmetic(arg1)

        elif parser.command_type() == Parser.C_POP or parser.command_type() == Parser.C_PUSH:
            arg2 = parser.arg2()
            code_writer.write_push_pop(command, arg1, arg2)


if __name__ == '__main__':
    # main()
    main()