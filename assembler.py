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
    global is_flag
    if reg == "FLAGS" and is_flag:
        is_flag = 0
        return registers[reg]
        
    elif reg != "FLAGS":
        if reg in registers:
            return registers[reg]
        else:
            print_error('Register not Found')
            exit()
    else:
        print_error('Illegal use of FLAGS register')
        exit()

def is_reg(register):
    return 1 if register in registers else 0
    
def get_ins_opcode(ins, ins_type):    
    if ins_type in instructions and ins in instructions[ins_type]:
        return instructions[ins_type][ins]
    else:
        print_error("Instruction not Found")
        exit()
        
def is_mem(var):
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
    global var_counter, variables_list
    
    if(var_check == 1):
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

def get_type(ins):
    if len(ins) == 1:
        ins_type = "F"
        if get_ins_opcode(ins[0], ins_type):
            return "F"
        else:
            print_error("General Syntax Error")
            exit()

    
    elif len(ins) == 2:
        ins_type = "E"
        if get_ins_opcode(ins[0], ins_type):
            return "E"
        else:
            print_error("General Syntax Error")
            exit()
    
    elif len(ins) == 3:
        if ins[-1][0] == "$":
            ins_type = "B"
            if get_ins_opcode(ins[0], ins_type):
                return "B"
            
        elif is_reg(ins[-1]):
            ins_type = "C"
            if get_ins_opcode(ins[0], ins_type):
                return "C"
            
        elif is_mem(ins[-1]):
            ins_type = "D"
            if get_ins_opcode(ins[0], ins_type):
                return "D"
        
        else:
            print_error("General Syntax Error")
            exit()
        
    elif len(ins) == 4:
        ins_type = "A"
        if get_ins_opcode(ins[0], ins_type):
            return "A"
        else:
            print_error("General Syntax Error")
            exit()
    
    else:
        print_error("General Syntax Error")
        exit()

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
    elif(ins_type == "C"):
        if ins[2] == "FLAGS":
            is_flag = 1
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*5}{get_register_address(ins[1])}{get_register_address(ins[2])}\n"
    elif(ins_type == "D"):
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*1}{get_register_address(ins[1])}{get_mem_addr(ins[2], ins_type)}\n"
    elif(ins_type == "E"):
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*4}{get_mem_addr(ins[1], ins_type)}\n"
    elif(ins_type == "F"):
        bit_ins = f"{get_ins_opcode(ins[0], ins_type)}{'0'*11}"   
    return bit_ins

def check_labels():
    global assembly_code
    label_counter = 0
    total_var = 0
    
    for ins in assembly_code:
        ins = ins.split(' ')
        if ins[0][-1] == ":":
            if len(ins[0].split(' ')) == 1:
                labels[ins[0][:-1]] = int_bits(label_counter - total_var)
                assembly_code[label_counter] = assembly_code[label_counter].replace(ins[0], "")
                
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
def get_mem_addr(var, ins_type):
    if ins_type == "D":
        if is_label_present(var):
            print_error("Misuse of labels as variables")
            exit()
        if is_var_present(var):
            return variables[var]
        else:
            print_error("Use of undefined variables")
            exit()
    
    elif ins_type == "E":
        if is_var_present(var):
            print_error("Misuse of variables as labels")
            exit()
        if is_label_present(var):
            return labels[var]
        else:
            print_error("Use of Undefined labels")
            exit()          
assembly_code = []
machine_code=[]

variables = {}
variables_list = []
labels = {}
is_flag = 0
var_counter=0
hlt_check = 0
program_counter = 0
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_help()
        exit(1)

    filename = sys.argv[1]
    
    if filename not in os.listdir():
        print_error("File not found")
        exit(1)

    with open(filename) as f:
        for line in f:
            if line.strip('\n') != '':
                assembly_code.append(line.strip('\n'))
        
    check_labels()   
    
    
    for line in assembly_code:
        line = line.split()
        if line[0] == "var":
            check_var(line, var_check)
        else:
            var_check = 1
            var_addr = len(assembly_code) - var_counter
            assign_variables(variables_list,var_addr)
            
        if line[0] == "hlt":
            hlt_check = 1
            if program_counter != len(assembly_code) - 1:
                print_error("hlt not being used as the last instruction")
                exit()
                             
        if line[0] != "var":
            ins_type = get_type(line)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            machine_code.append(convert_bits(line, ins_type))
                
            program_counter += 1
            
        if hlt_check != 1:
            print_error("Missing hlt instruction")                                                                                                                                                                                                                                                                                                                                                                                                  
            exit()        