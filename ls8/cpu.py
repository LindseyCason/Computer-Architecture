"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 #8 bit
        self.pc = 0 #index or program counter
        self.ram = [0] * 256 #Memory

    def load(self, progname):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # progname=sys.argv[1]

        with open(progname) as f:
            for line in f:
                # print(line)
                line=line.split("#")[0]
                line=line.strip() #get rid of whitespace
                if line == "":
                    continue
                # value=int(line)
                self.ram[address] = int(line, 2)
                # print("split-->",value)
                address +=1

        # program = [
        #     # From print8.ls8
        #     # 0b10000010, # LDI R0,8
        #     # 0b00000000,
        #     # 0b00001000,
        #     # 0b01000111, # PRN R0
        #     # 0b00000000,
        #     # 0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR]=MDR

    def run(self):
        """Run the CPU."""
        halted=False
        sp=255
        # print("THE RAM",self.ram)
        while halted == False:
            # sp_reg=7 #highest reg most recently pushed
            ir=self.ram_read(self.pc) #READ THE CURRENT PC AND STORE VALUE
            operand_a=self.ram_read(self.pc +1) #SAVE IN CASE NEEDED
            operand_b=self.ram_read(self.pc +2) #SAVE IN CASE NEEDED
            pc_inc=(int(ir) >>6) +1

            if ir == 0b10000010 or ir == "LDI": #130
                self.reg[operand_a]= operand_b
                self.pc+=pc_inc
            elif ir == 0b01000111 or ir == "PRN":
                # print(self.reg[operand_a])
                print(int(f"{self.reg[operand_a]}",10))
                self.pc +=pc_inc
            elif ir == 0b10100010 or ir == "MUL":
                self.alu("MUL", operand_a, operand_b)
                self.pc += pc_inc
            elif ir == 0b01000101 or ir == "PUSH":
                sp -= 1 #decrement pointer
                self.ram_write(self.reg[operand_a], sp) #self.ram?
                self.pc += pc_inc #increase CP by 2 bites
                self.reg[operand_a]=self.ram[operand_a]
            elif ir == 0b01000110 or ir == "POP":
                ## #01000110 # POP R2
                #-  00000010
                self.reg[operand_a] = self.ram_read(sp)
                sp +=1
                self.pc += pc_inc
            elif ir == 0b00000001 or ir == "HLT":
                print("Exiting")
                halted=True
                sys.exit(1)
        
