from my_parser import Parser
from symbol_table import SymbolTable
import code


def create_output_dir(input_dir):
    """ creates the output file directory based on the input directory """
    index = input_dir.rfind('asm')
    return input_dir[:index] + 'hack'


def create_c_bin_instruction(parser):
    """
    this function is called only if the current instruction's type
    returns the binary representation
    """
    dest_field, comp_field, jump_field = parser.dest(), parser.comp(), parser.jump()
    dest_bits, comp_bits, jump_bits = code.dest(dest_field), code.comp(comp_field), code.jump(jump_field)
    return '111' + comp_bits + dest_bits + jump_bits


def initialize(input_dir):
    """ constructs a new parser and a new symbol table """
    return Parser(input_dir), SymbolTable()


def create_symbol_table(parser, symbol_table):
    """ saves each symbol in the symbol_table and gives it a value """
    next_instruction_index = 0
    while parser.has_more_lines():
        parser.advance()
        if parser.instruction_type() == Parser.COMMENT_OR_EMPTY:
            continue

        if parser.instruction_type() == Parser.L_INSTRUCTION:
            symbol = parser.symbol(Parser.L_INSTRUCTION)
            symbol_table.add_entry(symbol, next_instruction_index)

        else:
            next_instruction_index += 1


def main():
    # initialize vars
    input_dir = 'C:\\Users\\User\\coding\\nand2tetris\\projects\\06\\rect\\Rect.asm'
    parser = Parser(input_dir)
    symbol_table = SymbolTable()

    # first pass. scan the entire program and add each label declaration to the symbol table
    create_symbol_table(parser, symbol_table)

    # reinitialize the parser to start reading the file from its start
    parser = Parser(input_dir)
    var_index = 16
    output_dir = create_output_dir(input_dir)
    output_file = open(output_dir, 'w')

    while parser.has_more_lines():
        binary_instruction = ''
        parser.advance()
        instruction_type = parser.instruction_type()

        if instruction_type == Parser.COMMENT_OR_EMPTY or instruction_type == Parser.L_INSTRUCTION:
            continue

        if instruction_type == Parser.A_INSTRUCTION:
            symbol = parser.symbol(instruction_type)
            if symbol.isnumeric() and 0 <= int(symbol) <= 32767:
                address = symbol
            else:
                if not symbol_table.contains(symbol):
                    symbol_table.add_entry(symbol, var_index)
                    var_index += 1
                address = symbol_table.get_address(symbol)
            binary_instruction = code.a_to_binary(address).zfill(16)

        elif instruction_type == Parser.C_INSTRUCTION:
            binary_instruction = create_c_bin_instruction(parser)

        output_file.write(binary_instruction + '\n')

    output_file.close()


if __name__ == '__main__':
    main()
