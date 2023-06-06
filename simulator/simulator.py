#! python3
import sys

# f = open('output.txt', 'w')

class Memory:
    mem = []
    
    def initialize(self):
        # with open("./test.txt") as f:
        #     for line in f:
        #         self.mem.append(line.strip('\n'))
                
        for ins in sys.stdin:
            self.mem.append(ins.strip())
            
        if(len(self.mem) < 128):
            for i in range(len(self.mem), 128):
                self.mem.append('0'*16)        
        
    
    def fetchData(self, PC):
        return self.mem[PC.counter]
    
    def mem_write(self, line, data):
        self.mem[line] = data   
    
    def dump(self):
        for ins in self.mem:
            # print(ins)
            # f.write(ins + "\n")
            sys.stdout.write(f"{ins}\n")
    class Opcodes:
        instructions = {
        "A": {
            "add": "00000",
            "sub": "00001",
            "mul": "00110",
            "xor": "01010",
            "or": "01011",
            "and": "01100",
            "addf": "10000",
            "subf": "10001",
            "rsb": "10100"
        },
        "B": {
            "mov": "00010",
            "rs": "01000",
            "ls": "01001",
            "movf": "10010",
            "dec": "10110",
            "inc": "10011",
            "cmn": "10111" 
            
        },
        "C": {
            "mov": "00011",
            "div": "00111",
            "not": "01101",
            "cmp": "01110"
        },
        "D": {
            "ld": "00100",
            "st": "00101",
            "swp": "10101"
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
    
    def getIns(self, opcode):
        for types in self.instructions:
            for ins in self.instructions[types]:
                if self.instructions[types][ins] == opcode:
                    return types, ins

class RegisterFile:
    register_memory = ["0"*16 for _ in range(8)]
    
    regs = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111"
    }
    
    def dump(self):
        # print(self.register_memory)
        for d in self.register_memory:
            # print(d, end=" ")
            # f.write(d + " ")
            sys.stdout.write(f"{d} ")
            
        # print()
        # f.write("\n")
        sys.stdout.write(f"\n")
        
        
    def reg_write(self, reg, data):
        self.register_memory[reg] = data

    def flags_reset(self):
        self.reg_write(7, "0"*16)    
    
class ProgramCounter:
    def _init_(self, counter):
        self.counter = counter
        
    def dump(self):
        # print(f"{self.counter:07b}", end=" ")
        sys.stdout.write(f"{self.counter:07b} ")
        # f.write(f"{self.counter:07b}" + " ")
        
    def update(self, counter):
        self.counter = counter