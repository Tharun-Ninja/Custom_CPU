#! python3
import sys
import os


def print_help():
    print("Usage: python3 main.py <text_file>")


def print_error(error):
    with open('error.txt', 'w') as e:
        e.write(f"Error in Line {program_counter + 1}: {error}\n")

    print(f"Error in Line {program_counter + 1}: {error}")


# list of registers
registers = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111"
}

# list of opcode
instructions = {
    "A": {
        "add": "00000",
        "sub": "00001",
        "mul": "00110",
        "xor": "01010",
        "or": "01011",
        "and": "01100"
    },
    "B": {
        "mov": "00010",
        "rs": "01000",
        "ls": "01001"
    },
    "C": {
        "mov": "00011",
        "div": "00111",
        "not": "01101",
        "cmp": "01110"
    },
    "D": {
        "ld": "00100",
        "st": "00101"
    },
    "E": {
        "jmp": "01111",
        "jlt": "11100",
        "jgt": "11101",
        "je": "11111"
    },
    "F": {
        "hlt": "11010"
    }
}

oper_param = {
    "A": 3,
    "B": 2,
    "C": 2,
    "D": 2,
    "E": 1,
    "F": 0
}

valid_operands = [key2 for key in instructions for key2 in instructions[key]]


def is_valid_operand(oper):
    if oper in valid_operands:
        return 1
    else:
        return 0

def get_param_len(oper):
    for key in instructions:
        if oper in list(instructions[key].keys()):
            # oper_type = key
            return key, oper_param[key]
    
    
# return the addr of register


def get_register_address(reg):
    """return the address of the register

    Args:
        reg (string): register name

    Returns:
        string: string of bits
    """

    global is_flag
    if reg == "FLAGS" and is_flag:
        is_flag = 0
        return registers[reg]

    elif reg != "FLAGS":
        if reg in registers:
            return registers[reg]
        else:
            print_error(f'{reg} is not a register')
            exit()
    else:
        print_error('Illegal use of FLAGS register')
        exit()


def is_reg(register):
    return 1 if register in registers else 0

# get the opcode of the instruction


def get_ins_opcode(ins, ins_type):
    """returns the opcode of the instructions to the corresponding
    type

    Args:
        ins (string): first word of the instruction
        ins_type (string): type of that instruction

    Returns:
        string: opcode of that instruction
    """
    if ins_type in instructions and ins in instructions[ins_type]:
        return instructions[ins_type][ins]
    else:
        print_error("Instruction not Found")
        print_error("Invalid operand")
        exit()


def is_mem(var):
    """checks variable syntax

    Args:
        addr (string): variable 

    Returns:
        int: 1 if variable syntax is good else error
    """
    if var[0].isalpha():
        return 1
    else:
        print_error("General Syntax Error")
        exit()


def is_var_present(var):
    if var in variables:
        return 1
    else:
        return 0


def check_var(ins, var_check):
    """Checks if the variable is proper and adds it to the dict

    Args:
        ins (string): list of ins
        var_check (int): is the variable acceptable
    """
    global var_counter, variables_list

    if (var_check == 1):
        print_error("Variables not declared at the beginning")
        exit()

    if ins[0] == "var" and len(ins) == 2:
        if is_var_present(ins[0]):
            print_error("Duplicate variable")
            exit()
        else:
            variables_list.append(ins[1])
            var_counter += 1


def assign_variables(variables_list, var_addr):
    for x in variables_list:
        variables[x] = int_bits(var_addr)
        var_addr += 1


def get_mem_addr(var, ins_type):
    if ins_type == "D":

        if is_var_present(var):
            return variables[var]
        else:
            print_error(f"No variable named \"{var}\"")
            exit()

    elif ins_type == "E":

        if is_label_present(var):
            return labels[var]
        else:
            print_error(f"No label named \"{var}\"")
            exit()


def get_type(ins):
    """returns the type of instruction

    Args:
        ins (list): list of the ins

    Returns:
        string: type of instruction
    """
    if not is_valid_operand(ins[0]):
        print_error(f"{ins[0]} is invalid operand")
        exit()
        
    ins_type, len_param = get_param_len(ins[0])
    
    if len(ins) - 1 != len_param:
        print_error(f"{ins[0]} must contain {len_param} parameters")
        exit()
        
    if ins[0] == "mov":
        if is_reg(ins[1]) and is_reg(ins[2]):
            ins_type = "C"
        else:
            ins_type = "B"
             
    return ins_type


def int_bits(data):
    """converts Imm value to 7 bits

    Args:
        data (int): Imm value

    Returns:
        string: bits of that integer
    """
    try:
        data = int(data)
    except:
        print_error(f"{data} is not an integer")
        exit()

    if (data >= 0 and data <= 127):
        return f'{data:07b}'
    else:
        print_error("Illegal Immediate values (more than 7 bits)")
        exit()


def convert_bits(ins, ins_type):
    """convert the instruction line to bits

    Args:
        ins (list): list of the instructions
        ins_type (string): type of the instruction

    Returns:
        string: string of bits of the instruction
    """
    global is_flag
    bit_ins = ""

    if (ins_type == "A"):
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*2}{get_register_address(ins[1])}{get_register_address(ins[2])}{get_register_address(ins[3])}\n"
    elif (ins_type == "B"):
        if ins[2][0] != "$":
            print_error(f"\"{ins[2]}\" in not defined")
            exit()
            
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*1}{get_register_address(ins[1])}{int_bits(ins[2][1:])}\n"
    elif (ins_type == "C"):
        if ins[2] == "FLAGS":
            is_flag = 1
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*5}{get_register_address(ins[1])}{get_register_address(ins[2])}\n"
    elif (ins_type == "D"):
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*1}{get_register_address(ins[1])}{get_mem_addr(ins[2], ins_type)}\n"
    elif (ins_type == "E"):
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*4}{get_mem_addr(ins[1], ins_type)}\n"
    elif (ins_type == "F"):
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*11}"
    return bit_ins


def check_labels():
    """Finds the labels and 
    allocates memory address to the labels in the
    dictionary
    """
    global assembly_code
    label_counter = 0
    total_var = 0

    for ins in assembly_code:
        ins = ins.split(' ')
        # print("label", ins)
        if ":" in ins[0]:
            if len(ins[0].split(' ')) == 1:
                # print(ins[0][:ins[0].index(":")])
                labels[ins[0][:ins[0].index(":")]] = int_bits(label_counter - total_var)
                assembly_code[label_counter] = assembly_code[label_counter].replace(ins[0][:ins[0].index(":")+1], "")

            else:
                print_error("label not properly spaced")

        if ins[0] == "var":
            total_var += 1

        label_counter += 1


def is_label_present(var):
    if var in labels:
        return 1
    else:
        return 0


# Stores assembly and machine code
assembly_code = []
machine_code = []

# Stores the list of variables and labels
variables = {}
variables_list = []
labels = {}

# checkers for finding duplicate variable and hlt ins
is_flag = 0
var_counter = 0
hlt_check = 0
var_check = 0

# Tracks the current executing line
program_counter = 0

if __name__ == "__main__":
    # print(sys.argv)
    # if len(sys.argv) != 2:
    #     print_help()
    #     exit()
    
    

    # Get filename
    # filename = sys.argv[1]

    # Store all the lines in assembly code
    # try:
    #     with open(filename) as f:
    #         for line in f:
    #             if line.strip('\n') != '':
    #                 assembly_code.append(line.strip('\n'))
    # except:
    #     print_error("File not found")
    #     exit()
    for ins in sys.stdin:
        assembly_code.append(ins)

    check_labels()

    for line in assembly_code:

        line = line.split()
        # print(line)

        if line == []:
            program_counter -= 1
            continue

        if line[0] == "var":
            check_var(line, var_check)
        else:
            var_check = 1
            var_addr = len(assembly_code) - var_counter
            assign_variables(variables_list, var_addr)

        if line[0] == "hlt":
            hlt_check = 1
            if program_counter != len(assembly_code) - 1:
                print_error("hlt not being used as the last instruction")
                exit()

        if line[0] != "var":
            ins_type = get_type(line)
            machine_code.append(convert_bits(line, ins_type))

        program_counter += 1

    # check missing hlt instruction
    if hlt_check != 1:
        print_error("Missing hlt instruction")
        exit()

    if len(machine_code) > 128:
        print_error("Assembler can only work with 128 lines")
        exit()

    # with open('machine_code.txt', 'w') as w:
    #     w.writelines(machine_code)
    #     with open('error.txt', 'w') as e:
    #         pass
        
    for lin in machine_code:
        sys.stdout.write(lin)
