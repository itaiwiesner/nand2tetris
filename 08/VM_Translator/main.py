from code_writer import CodeWriter
from vm_parser import Parser
import sys
import os


class VMTranslator:
    def __init__(self, output_path):
        self.parser = None
        self.code_writer = CodeWriter(output_path)
        self.code_writer.write_init()

    def close(self):
        self.code_writer.close()
    
    def translate(self, input_path):
        self.parser = Parser(input_path)
        print(self.parser.current_command)
        while self.parser.has_more_lines_advance():
            command_type = self.parser.command_type()
            if command_type == 'COMMENT_OR_EMPTY':
                continue

            if command_type == 'C_RETURN':
                self.code_writer.write_return()
                continue

            # self.parser.arg1() = self.parser.self.parser.arg1()()

            if command_type in self.parser.ARG2_COMMANDS:
                # self.parser.arg2() = self.parser.self.parser.arg2()()
                match command_type:
                    case 'C_FUNCTION':
                        self.code_writer.write_function(self.parser.arg1(), self.parser.arg2())
                    case 'C_CALL':
                        self.code_writer.write_call(self.parser.arg1(), self.parser.arg2())
                    case 'C_PUSH':
                        self.code_writer.write_push(self.parser.arg1(), self.parser.arg2())
                    case 'C_POP':
                        self.code_writer.write_pop(self.parser.arg1(), self.parser.arg2())

            else:
                match command_type:
                    case 'C_ARITHMETIC':
                        self.code_writer.write_arithmetic(self.parser.arg1())
                    case 'C_LABEL':
                        self.code_writer.write_label(self.parser.arg1())
                    case 'C_GOTO':
                        self.code_writer.write_goto(self.parser.arg1())
                    case 'C_IF':
                        self.code_writer.write_if(self.parser.arg1())


if __name__ == '__main__':
    root = 'C:\\Users\\User\\coding\\nand2tetris\\projects\\08\\ProgramFlow\\BasicLoop\\BasicLoop.vm'
    # root = sys.argv[-1]
    if root.endswith('.vm'):
        output_file = f'{root[:-2]}asm'
    else:
        output_file = f'{root}.asm'

    vm_translator = VMTranslator(output_file)
    if os.path.isdir(root):
        for file in os.listdir(root):
            input_file = fr'{root}\{file}'
            vm_translator.translate(input_file)

    else:
        input_file = root
        vm_translator.translate(input_file)

    vm_translator.close()
