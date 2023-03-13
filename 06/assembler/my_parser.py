
class Parser:
    TYPES = {'A_INSTRUCTION': 'A_INSTRUCTION', 'C_INSTRUCTION': 'C_INSTRUCTION', 'L_INSTRUCTION': 'L_INSTRUCTION'}
    A_INSTRUCTION = 'A_INSTRUCTION'
    C_INSTRUCTION = 'C_INSTRUCTION'
    L_INSTRUCTION = 'L_INSTRUCTION'
    COMMENT_OR_EMPTY = 'COMMENT_OR_EMPTY'

    def __init__(self, file):
        self.file = open(file)
        self.lines = self.lines_gen()
        self.current_line = None

    def lines_gen(self):
        """ a generator function that creates a generator of lines in the file """
        for line in self.file:
            # print(line, end='')
            yield line

    def has_more_lines(self):
        """ checks if the current line is the last one """
        try:
            self.current_line = next(self.lines)
            return True
        except StopIteration:
            self.file.close()
            return False

    def advance(self):
        """
        reads the next line and makes it the current instruction.
        removes whitespaces and commented text
        """
        if self.current_line.endswith('\n'):
            self.current_line = self.current_line[:-1]
        self.current_line = self.current_line.replace(' ', '')
        self.current_line = self.current_line.split('//')[0]

    def instruction_type(self):
        """
        given a valid instruction, the function returns weather it's A, C or L instruction or a comment/empty line
        """
        if self.current_line == '':
            return Parser.COMMENT_OR_EMPTY

        if self.current_line.startswith('@'):
            return Parser.A_INSTRUCTION

        if self.current_line.startswith('('):
            return Parser.L_INSTRUCTION

        return Parser.C_INSTRUCTION

    def symbol(self, instruction_type):
        """
        this function is called only if instruction_type is L or A instruction
        if the current instruction is L, returns the symbol
        if the current instruction is A, returns the symbol or decimal (as a string)
        """
        if instruction_type == Parser.A_INSTRUCTION:
            return self.current_line[1:]
        elif instruction_type == Parser.L_INSTRUCTION:
            return self.current_line[1:-1]

    def dest(self):
        """
        this function is called only if instruction_type is C_INSTRUCTION
        returns the destination field part of the current C_instruction
        """
        return '' if '=' not in self.current_line else self.current_line.split('=')[0]

    def comp(self):
        """
        this function is called only if instruction_type is C_INSTRUCTION
        returns the comp field part of the current C_instruction
        """
        not_dest_field = self.current_line.split('=')[-1]
        comp_field = not_dest_field.split(';')[0]
        return '' if len(comp_field) == 0 else comp_field

    def jump(self):
        """
        this function is called only if instruction_type is C_INSTRUCTION
        returns the jump field part of the current C_instruction
        """
        return '' if ';' not in self.current_line else self.current_line.split(';')[-1]
