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

def get_register_address(reg):
    global registers
    if reg in registers:
        return registers[reg]
    else:
        print_error('Register not Found')
        exit()

def is_reg(register):
    return 1 if register in registers else 0
    
def get_ins_opcode(ins, ins_type):    
    if ins_type in instructions and ins in instructions[ins_type]:
        return instructions[ins_type][ins]
    else:
        print_error("Instruction not Found")
        exit()



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
        print_error("General Syntax Error")
        exit()
        
    if(data >= 0 and data <= 127):  
        return f'{data:07b}'
    else:
        print_error("Illegal Immediate values (more than 7 bits)")
        exit()

def convert_bits(ins, ins_type):
    bit_ins = ""
    if(ins_type == "A"):
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*2}{get_register_address(ins[1])}{get_register_address(ins[2])}{get_register_address(ins[3])}\n"
    elif(ins_type == "B"):
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*1}{get_register_address(ins[1])}{int_bits(ins[2][1:])}\n"   
        
    return bit_ins


machine_code=[]

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
    
    with open(filename) as f:
        for line in f:
            line = line.strip().split(' ')
            if line[0] != "var":
                ins_type = get_type(line)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                machine_code.append(convert_bits(line, ins_type))
                
            program_counter += 1
        