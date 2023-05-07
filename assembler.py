#! python3
import sys
import os


def print_help():
    print("Usage: python3 assembler.py <text_file>")
    
def print_error(error):
    print(f"Error: {error}")
    
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


def get_register_address(reg):
    global registers
    if reg in registers:
        return registers[reg], 0
    else:
        print_error('Register not Found')
        return "", 1

def is_reg(register):
    return 1 if register[reg] else 0
    
def get_ins_opcode(ins, ins_type):
    print(ins)
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
    
    if ins_type in instructions and ins in instructions[ins_type]:
        return instructions[ins_type][ins] , 0
    else:
        print_error("Instruction not Found")
        return "" , 1



def get_type(ins):
    if len(ins) == 1:
        return "F"
    
    elif len(ins) == 2:
        return "E"
    
    elif len(ins) == 3:
        if ins[-1][0] == "$":
            return "B"
        elif is_reg(ins[-1]):
            return "C"
        elif 1:
            return "D" # need to check mem type 
        else:
            # Throw error
            pass
        
    elif len(ins) == 4:
        return "A"
    
    else:
        # Throw error
        pass
    
def create_ins_bits(ins, ins_type):
    bit_ins = ""
    check = 0
    if ins_type == "A":
        print('hi')
        try:
            print(ins[0], ins_type)
            bit_ins, check = get_ins_opcode(ins[0], ins_type)
            print(bit_ins, check)
            return bit_ins, check
        except:
            exit()
    elif ins_type == "B":
        print('hi')
        try:
            print(ins[0], ins_type)
            bit_ins, check = get_register_address(ins[1])
            print(bit_ins, check)
            return bit_ins, check
        except:
            pass
            # exit()
        
        


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_help()
        exit(1)

    filename = sys.argv[1]
    
    if filename not in os.listdir():
        print_error("File not found")
        exit(1)

    program_counter = 0
    current_ins = ""
    # with open(filename) as f:
    #     for line in f:
    #         line = line.strip().split(' ')
    #         program_counter += 1
    #         print(line)
    #         if line[0] != 'var' and line[0] != '':
    #             ins_type = get_type(line)
    #             current_ins = create_ins_bits(line, ins_type)
                

    # print(f"Total lines: {program_counter}")
    
    current_ins, check = create_ins_bits(['mov', 'R22', '$10'], "B")
    print(current_ins, check)
    print("hihsf")

    print("checking.... ")

    
print("checking again")


print("Checking again")