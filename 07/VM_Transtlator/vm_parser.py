class Parser:
    COMMENT_OR_EMPTY = 'COMMENT_OR_EMPTY'
    C_ARITHMETIC = 'C_ARITHMETIC'
    C_PUSH = 'C_PUSH'
    C_POP = 'C_POP'
    C_LABEL = 'C_LABEL'
    C_GOTO = 'C_GOTO'
    C_IF = 'C_IF'
    C_FUNCTION = 'C_FUNCTION'
    C_RETURN = 'C_RETURN'
    C_CALL = 'C_CALL'
    ARITHMETIC_OPTIONS = ('add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not')

    def __init__(self, file):
        self.file = open(file)
        self.lines = self.lines_gen()
        self.current_command = None

    def lines_gen(self):
        """ a generator function that creates a generator of lines in the file """
        for line in self.file:
            yield line

    def has_more_lines_advance(self):
        """
        make the next line the current_command.
        skips over comments and white spaces"""
        try:
            self.current_command = next(self.lines)

        except StopIteration:
            self.file.close()
            return False

        else:
            return True

    def is_command(self):
        """ returns if the given line is a valid command or a comment/whitespaces """
        if self.current_command.endswith('\n'):
            self.current_command = self.current_command[:-1]
        self.current_command = self.current_command.strip()
        self.current_command = self.current_command.split('//')[0]
        print(self.current_command)
        return len(self.current_command) != 0

    def command_type(self):
        """ returns the constant representing the type of the current command """
        if len(self.current_command) == 0:
            return Parser.COMMENT_OR_EMPTY

        if self.current_command in Parser.ARITHMETIC_OPTIONS:
            return Parser.C_ARITHMETIC

        if self.current_command.startswith('push'):
            return Parser.C_PUSH

        if self.current_command.startswith('pop'):
            return Parser.C_POP

    def arg1(self):
        """
        returns the first argument of the current command.
        in case of C_ARITHMETIC the command itself is returned.
        shouldn't be called if the current command is C_RETURN
        """
        if self.command_type() == Parser.C_ARITHMETIC:
            return self.current_command
        return self.current_command.split()[1]

    def arg2(self):
        """
        returns the second argument of the current command.
        should be called only if command type isn't C_ARITHMETIC or C_RETURN
        """
        return int(self.current_command.split()[-1])
