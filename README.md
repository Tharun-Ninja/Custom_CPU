# ComputerOrganizationAssignment

### Custom Instructions 
| Opcode | Instruction | Semantics | Syntax | Type |
|:------:|:-----------:|:---------:|:------:|:----:|
| 10100  | Reverse Subraction | Performs reg1 = reg3 - reg2. In case reg2 > reg3, 0 is written to reg1 and overflow flag is set. | rsb reg1 reg2 reg3 | A |
| 10110  | Decrement by Imm | Performs reg1 = reg1 - Imm| dec reg1 $Imm | B |
| 10011  | Increment by Imm | Performs reg1 = reg1 + Imm | inc reg1 $Imm | B |
| 10111  | Compares the register with Imm | Compares reg1 and Imm, sets up the FLAGS register.| cmn reg1 $Imm | B |
| 10101  | Swap the data in register and memory | Performs reg1,mem_addr = mem_addr, reg1 | swp reg1 mem_addr | D |