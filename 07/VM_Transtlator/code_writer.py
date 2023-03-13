import os


class CodeWriter:
    SEGMENT_TO_ADDRESS = {
        'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'
    }
    
    def __init__(self, output_file):
        self.file = open(output_file, 'w')
        self.label_index = 0

    def write_arithmetic(self, command):
        """
        writes to the output file the assembly code that implements the given arithmetic command
        """
        # generate the comment
        output = f'//{command}\n'

        if command == 'add':
            output += '@SP\n'
            output += 'M=M-1\n'
            output += 'A=M\n'
            output += 'D=M\n'
            output += 'A=A-1\n'
            output += 'M=D+M\n'

        elif command == 'sub':
            output += '@SP\n'
            output += 'M=M-1\n'
            output += 'A=M\n'
            output += 'D=M\n'
            output += 'A=A-1\n'
            output += 'M=M-D\n'

        elif command == 'neg':
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'M=-M\n'

        elif command == 'eq':
            label = f'EQ{self.label_index}'
            output += '@SP\n'
            output += 'M=M-1\n'
            output += 'A=M\n'
            output += 'D=M\n'
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'D=D-M\n'
            output += 'M=-1\n'
            output += f'@{label}\n'
            output += 'D;JEQ\n'
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'M=0\n'
            output += f'{label}\n'
            self.label_index += 1

        elif command == 'gt':
            label = f'GT{self.label_index}'
            output += '@SP\n'
            output += 'M=M-1\n'
            output += 'A=M\n'
            output += 'D=M\n'
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'D=M-D\n'
            output += 'M=-1\n'
            output += f'@{label}\n'
            output += 'D;JGT\n'
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'M=0\n'
            output += f'{label}\n'
            self.label_index += 1

        elif command == 'lt':
            label = f'LT{self.label_index}'
            output += '@SP\n'
            output += 'M=M-1\n'
            output += 'A=M\n'
            output += 'D=M\n'
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'D=M-D\n'
            output += 'M=-1\n'
            output += f'@{label}\n'
            output += 'D;JLT\n'
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'M=0\n'
            output += f'{label}\n'
            self.label_index += 1

        elif command == 'and':
            output += '@SP\n'
            output += 'M=M-1\n'
            output += 'A=M\n'
            output += 'D=M\n'
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'M=D&M\n'

        elif command == 'or':
            output += '@SP\n'
            output += 'M=M-1\n'
            output += 'A=M\n'
            output += 'D=M\n'
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'M=D|M\n'

        elif command == 'not':
            output += '@SP\n'
            output += 'A=M-1\n'
            output += 'M=!M\n'

        self.file.write(output)

    def write_push_pop(self, command, segment, index):
        """
        writes to the output file the assembly code that implements the given command.
        the command is either C_PUSH or C_POP
        """
        address = ''
        name = os.path.basename(self.file.name).split('.')[0]
        # write the comment
        output = f'//{command} {segment} {index}\n'

        if command == 'push':
            if segment in CodeWriter.SEGMENT_TO_ADDRESS:
                address = CodeWriter.SEGMENT_TO_ADDRESS[segment]
                output += f'@{index}\n'
                output += 'D=A\n'
                output += f'@{address}\n'
                output += 'A=D+M\n'
                output += 'D=M\n'
                output += '@SP\n'
                output += 'A=M\n'
                output += 'M=D\n'
                output += '@SP\n'
                output += 'M=M+1\n'

            elif segment == 'constant':
                output += f'@{index}\n'
                output += 'D=A\n'
                output += '@SP\n'
                output += 'A=M\n'
                output += 'M=D\n'
                output += '@SP\n'
                output += 'M=M+1\n'

            elif segment == 'static':
                output += f'@{name}.{index}\n'
                output += 'D=M\n'
                output += '@SP\n'
                output += 'A=M\n'
                output += 'M=D\n'
                output += '@SP\n'
                output += 'M=M+1\n'

            elif segment == 'temp':
                output += f'@{index + 5}\n'
                # output += 'A=M\n'
                output += 'D=M\n'
                output += '@SP\n'
                output += 'A=M\n'
                output += 'M=D\n'
                output += '@SP\n'
                output += 'M=M+1\n'

            elif segment == 'pointer':
                if index == 0:
                    address = 'THIS'
                elif index == 1:
                    address = 'THAT'

                output += f'@{address}\n'
                output += 'D=M\n'
                output += '@SP\n'
                output += 'A=M\n'
                output += 'M=D\n'
                output += '@SP\n'
                output += 'M=M+1\n'

        elif command == 'pop':
            if segment in CodeWriter.SEGMENT_TO_ADDRESS:
                address = CodeWriter.SEGMENT_TO_ADDRESS[segment]
                output += f'@{index}\n'
                output += 'D=A\n'
                output += f'@{address}\n'
                output += 'D=D+M\n'
                output += '@R13\n'
                output += 'M=D\n'
                output += '@SP\n'
                output += 'M=M-1\n'
                output += 'A=M\n'
                output += 'D=M\n'
                output += '@R13\n'
                output += 'A=M\n'
                output += 'M=D\n'

            elif segment == 'static':
                output += '@SP\n'
                output += 'M=M-1\n'
                output += 'A=M\n'
                output += 'D=M\n'
                output += f'@{name}.{index}\n'
                output += 'M=D\n'

            elif segment == 'temp':
                output += '@SP\n'
                output += 'M=M-1\n'
                output += 'A=M\n'
                output += 'D=M\n'
                output += f'@{5 + index}\n'
                # output += 'A=M\n'
                output += 'M=D\n'

            elif segment == 'pointer':
                if index == 0:
                    address = 'THIS'
                elif index == 1:
                    address = 'THAT'

                output += '@SP\n'
                output += 'M=M-1\n'
                output += 'A=M\n'
                output += 'D=M\n'
                output += f'@{address}\n'
                output += 'M=D\n'

        self.file.write(output)
