import os


class CodeWriter:
    SEGMENT_TO_ADDRESS = {
        'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'
    }

    def __init__(self, output_path):
        self.file = open(output_path, 'w')
        self.eq_index = 0
        self.gt_index = 0
        self.lt_index = 0
        self.return_index = 0

    def close(self):
        """ closes the output file """
        self.file.close()

    def write_init(self):
        """ writes the assembly instructions that effect the bootstrap code that initializes the VM """
        self.file.write('// Bootstrap code\n')
        self.file.write('@256\n')
        self.file.write('D=A\n')
        self.file.write('@SP\n')
        self.file.write('M=D\n')
        self.write_call('Sys.init', 0)

    def write_arithmetic(self, command):
        """
        writes to the output file the assembly code that implements the given arithmetic command
        """
        # generate the comment
        self.file.write(f'//{command}\n')

        if command == 'add':
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write('A=A-1\n')
            self.file.write('M=D+M\n')

        elif command == 'sub':
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write('A=A-1\n')
            self.file.write('M=M-D\n')

        elif command == 'neg':
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('M=-M\n')

        elif command == 'eq':
            label = f'EQ{self.eq_index}'
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('D=D-M\n')
            self.file.write('M=-1\n')
            self.file.write(f'@{label}\n')
            self.file.write('D;JEQ\n')
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('M=0\n')
            self.file.write(f'{label}\n')
            self.eq_index += 1

        elif command == 'gt':
            label = f'GT{self.gt_index}'
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('D=M-D\n')
            self.file.write('M=-1\n')
            self.file.write(f'@{label}\n')
            self.file.write('D;JGT\n')
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('M=0\n')
            self.file.write(f'{label}\n')
            self.gt_index += 1

        elif command == 'lt':
            label = f'LT{self.lt_index}'
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('D=M-D\n')
            self.file.write('M=-1\n')
            self.file.write(f'@{label}\n')
            self.file.write('D;JLT\n')
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('M=0\n')
            self.file.write(f'{label}\n')
            self.lt_index += 1

        elif command == 'and':
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('M=D&M\n')

        elif command == 'or':
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('M=D|M\n')

        elif command == 'not':
            self.file.write('@SP\n')
            self.file.write('A=M-1\n')
            self.file.write('M=!M\n')

    def write_push(self, segment, index):
        """ writes to the output file the assembly code that implements the given command push command """
        address = ''
        name = os.path.basename(self.file.name).split('.')[0]
        # write the comment
        self.file.write(f'// push {segment} {index}\n')

        if segment in CodeWriter.SEGMENT_TO_ADDRESS:
            address = CodeWriter.SEGMENT_TO_ADDRESS[segment]
            self.file.write(f'@{index}\n')
            self.file.write('D=A\n')
            self.file.write(f'@{address}\n')
            self.file.write('A=D+M\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')
            self.file.write('@SP\n')
            self.file.write('M=M+1\n')

        elif segment == 'constant':
            self.file.write(f'@{index}\n')
            self.file.write('D=A\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')
            self.file.write('@SP\n')
            self.file.write('M=M+1\n')

        elif segment == 'static':
            self.file.write(f'@{name}.{index}\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')
            self.file.write('@SP\n')
            self.file.write('M=M+1\n')

        elif segment == 'temp':
            self.file.write(f'@{index + 5}\n')
            # self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')
            self.file.write('@SP\n')
            self.file.write('M=M+1\n')

        elif segment == 'pointer':
            if index == 0:
                address = 'THIS'
            elif index == 1:
                address = 'THAT'

            self.file.write(f'@{address}\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')
            self.file.write('@SP\n')
            self.file.write('M=M+1\n')

    def write_pop(self, segment, index):
        """ writes to the output file the assembly code that implements the given command pop command """
        address = ''
        name = os.path.basename(self.file.name).split('.')[0]
        # write the comment
        self.file.write(f'// pop {segment} {index}\n')

        if segment in CodeWriter.SEGMENT_TO_ADDRESS:
            address = CodeWriter.SEGMENT_TO_ADDRESS[segment]
            self.file.write(f'@{index}\n')
            self.file.write('D=A\n')
            self.file.write(f'@{address}\n')
            self.file.write('D=D+M\n')
            self.file.write('@R13\n')
            self.file.write('M=D\n')
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write('@R13\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')

        elif segment == 'static':
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write(f'@{name}.{index}\n')
            self.file.write('M=D\n')

        elif segment == 'temp':
            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write(f'@{5 + index}\n')
            # self.file.write('A=M\n')
            self.file.write('M=D\n')

        elif segment == 'pointer':
            if index == 0:
                address = 'THIS'
            elif index == 1:
                address = 'THAT'

            self.file.write('@SP\n')
            self.file.write('M=M-1\n')
            self.file.write('A=M\n')
            self.file.write('D=M\n')
            self.file.write(f'@{address}\n')
            self.file.write('M=D\n')

    def write_label(self, label):
        """ Writes assembly code that effects the label command """
        # write the comment
        self.file.write(f'// label {label}\n')
        self.file.write(f'({label})\n')

    def write_goto(self, label):
        """ writes assembly code that effects the goto command """
        # write the comment
        self.file.write(f'// goto {label}\n')
        self.file.write(f'@{label}\n')
        self.file.write('0;JMP\n')

    def write_if(self, label):
        """ writes assembly code that effects the if-goto command """
        # write the comment
        self.file.write(f'// if-goto {label}\n')
        self.file.write('@SP\n')
        self.file.write('M=M-1\n')
        self.file.write('D=M\n')
        self.file.write(f'@{label}\n')
        self.file.write('D;JNE\n')

    def write_call(self, function_name, num_args):
        """ write assembly code that effects the call command """
        # write the comment
        self.file.write(f'// call {function_name} {num_args}\n')
        self.file.write(f'@{function_name}$ret{self.return_index}\n')
        self.file.write('D=A\n')
        self.file.write('@SP\n')
        self.file.write('A=M\n')
        self.file.write('M=D\n')
        self.file.write('@SP\n')
        self.file.write('M=M+1\n')

        # push frame
        for val in CodeWriter.SEGMENT_TO_ADDRESS.values():
            self.file.write(f'@{val}\n')
            self.file.write('D=M\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')
            self.file.write('@SP\n')
            self.file.write('M=M+1\n')

        # ARG = SP - 5 - num_args
        self.file.write('@SP\n')
        self.file.write('D=A\n')
        self.file.write('@5\n')
        self.file.write('D=D-A\n')
        self.file.write(f'@{num_args}\n')
        self.file.write('D=D-A\n')
        self.file.write('@ARG\n')
        self.file.write('M=D\n')

        # LCL = SP
        self.file.write('@SP\n')
        self.file.write('D=M\n')
        self.file.write('@LCL\n')
        self.file.write('M=D\n')

        # goto function_name
        self.write_goto(function_name)

        self.write_label(f'@{function_name}$ret{self.return_index}\n')

    def write_function(self, function_name, num_vars):
        """ write assembly code that effects the function command """
        # write the comment
        self.file.write(f'// function {function_name}\n')
        self.file.write(f'({function_name})\n')

        # initialize num_vars local variables to 0
        for index in range(num_vars):
            self.write_push('constant', 0)

    def write_return(self):
        """ write assembly code that effects the return command """
        # write the comment
        self.file.write('// return\n')

        # end_frame = LCL
        self.file.write('@LCL\n')
        self.file.write('D=A\n')
        self.file.write('@end_frame\n')
        self.file.write('M=D\n')

        # ret_addr = *(end_frame - 5)
        self.file.write('@end_frame\n')
        self.file.write('D=M\n')
        self.file.write('@5\n')
        self.file.write('A=D-A\n')
        self.file.write('D=M\n')
        self.file.write('@ret_addr\n')
        self.file.write('M=D\n')

        # *ARG = pop()
        self.write_pop('argument', 0)
        self.file.write('@ARG\n')
        self.file.write('D=A+1\n')
        self.file.write('@SP\n')
        self.file.write('M=D\n')

        # {THIS/THAT/ARG/LCL} = *(endFrame - {1/2/3/4})
        for segment in ['THAT', 'THIS', 'ARG', 'LCL']:
            self.file.write('@end_frame\n')
            self.file.write('A=A-1\n')
            self.file.write('D=M\n')
            self.file.write(f'@{segment}\n')
            self.file.write('M=D\n')

        self.file.write('@ret_addr\n')
        self.file.write('A=M\n')
        self.file.write('0;JMP\n')
