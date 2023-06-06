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
        
        
class ExecutionEngine:
    def bin_int(self, binary):
        return int(binary, 2)
    
    def int_bin(self, data):
            return f'{data:016b}'
        
    def ieee_fraction(self,data):
        e = data[:3]
        m = data[3:8]
        
        e = int(e, 2) - 4
        binary = f"1{m}"
        integer = int(binary[:e+1], 2)
        fraction = int(binary[e+1:], 2) / (2 ** len(binary[e+1:]))
        
        number = integer+fraction
        return number    

    def dec_ieee(self,data):
        number = int(data.split('.')[0])
        fraction = float(data) - number
        
        binary = f"{bin(number).replace('0b', '')}"
        e = len(binary) -1
        
        binary = binary[:1] + "." + binary[1:len(binary)]
        k_bits = 5 - e
        
        while (k_bits) :
            fraction *= 2
            fract_bit = int(fraction)
    
            if (fract_bit == 1) :
                fraction -= fract_bit
                binary += '1'
            else :
                binary += '0'
    
            k_bits -= 1
            
        e = bin(e+4).replace('0b','').rjust(3, "0")
        m = str(binary[2:])
        
        ieee = e + m
        return ieee
    
    def is_overflow(self,val):
        return 1 if (val > (2**16 - 1)) else 0

    
    def execute(self, instruction):
        opcode = instruction[0:5]
        type_ins, ins = Opcodes().getIns(opcode)
        
        if type_ins == "A":
            if ins != "addf" and ins != "subf":
                reg1 = self.bin_int(RF.register_memory[self.bin_int(instruction[7:10])])
                reg2 = self.bin_int(RF.register_memory[self.bin_int(instruction[10:13])])
                reg3 = self.bin_int(RF.register_memory[self.bin_int(instruction[13:16])])
                
                # print(reg1, reg2, reg3)
                if ins == "add":
                    reg1 = reg2 + reg3
                elif ins == 'sub':
                    reg1 = reg2 - reg3
                    if reg3 > reg2:
                        RF.reg_write(self.bin_int('111'), self.int_bin(8))
                    else:
                        RF.reg_write(self.bin_int(instruction[7:10]), self.int_bin(reg1))
                        
                    return False, PC.counter + 1
                elif ins == 'mul':
                    reg1 = reg2 * reg3
                elif ins == 'xor':
                    reg1 = reg2 ^ reg3
                elif ins == 'or':
                    reg1 = reg2 | reg3
                elif ins == 'and':
                    reg1 = reg2 & reg3  
                elif ins == 'rsb':
                    reg1 = reg3 - reg2
                    
                if self.is_overflow(reg1):
                    reg1 = 0
                    RF.reg_write(self.bin_int('111'), self.int_bin(8))
                else:    
                    RF.reg_write(self.bin_int(instruction[7:10]), self.int_bin(reg1))
            
                return False, PC.counter + 1
                     
            else:
                reg2 = self.ieee_fraction(RF.register_memory[self.bin_int(instruction[10:13])][8:])
                reg3 = self.ieee_fraction(RF.register_memory[self.bin_int(instruction[13:16])][8:])
                
                if ins == "addf":
                    reg1 = reg2 + reg3
                    if self.is_overflow(reg1):
                        reg1 = 0
                        RF.reg_write(self.bin_int('111'), self.int_bin(8))
                    else:
                        RF.reg_write(self.bin_int(instruction[7:10]), f"{'0'*8}{self.dec_ieee(str(reg1))}")
                    
                    return False, PC.counter + 1
                
                elif ins == "subf":
                    reg1 = reg2 - reg3
                    
                    if reg3 > reg2:
                        RF.reg_write(self.bin_int('111'), self.int_bin(8))
                    else:
                        RF.reg_write(self.bin_int(instruction[7:10]), self.dec_ieee(reg1))
                    return False, PC.counter + 1