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
            