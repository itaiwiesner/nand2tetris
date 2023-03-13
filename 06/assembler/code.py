JUMP_TO_BINARY = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
                  'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

COMP_TO_BINARY = {'': '000000', '0': '101010', '1': '111111', '-1': '111010', 'D': '001100', 'x': '110000',
                  '!D': '001101', '!x': '110001', '-D': '001111', '-x': '110011',
                  'D+1': '011111', 'x+1': '110111', 'D-1': '001110', 'x-1': '110010',
                  'D+x': '000010', 'D-x': '010011', 'x-D': '000111', 'D&x': '000000', 'D|x': '010101'
                  }


def a_to_binary(a_instruction):
    """ gets an A instruction (without @). converts to binary and returns """
    return str(int(bin(int(a_instruction))[2:]))


def dest(dest_field):
    """ returns the binary representation of the parsed dest field (string) """
    bit_a = str(int('A' in dest_field))
    bit_d = str(int('D' in dest_field))
    bit_m = str(int('M' in dest_field))
    return bit_a + bit_d + bit_m


def jump(jump_field):
    """ returns the binary representation of the parsed jump field (string) """
    return JUMP_TO_BINARY[jump_field]


def comp(comp_field):
    """ returns the binary representation of the parsed comp field"""
    a = str(int('M' in comp_field))
    comp_field = ''.join(['x' if i in 'AM' else i for i in comp_field])
    return str(a + COMP_TO_BINARY[comp_field])
