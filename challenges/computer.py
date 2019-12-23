class Computer:
    def __init__(self, intcode):
        self.intcode = intcode.copy()
        self.pointer = 0
        
        self.opcode_map = {
            1: (self.opcode_1, 3),
            2: (self.opcode_2, 3),
            99: (self.opcode_99, 0)
        }

    def opcode_1(self, params):
        value_1 = self.intcode[params[0]]
        value_2 = self.intcode[params[1]]
        result = value_1 + value_2
        self.intcode[params[2]] = result
        self.pointer += len(params) + 1
    

    def opcode_2(self, params):
        value_1 = self.intcode[params[0]]
        value_2 = self.intcode[params[1]]
        result = value_1 * value_2
        self.intcode[params[2]] = result
        self.pointer += len(params) + 1

    def opcode_99(self, params):
        raise StopIteration
    
    def run_iteration(self):
        opcode = self.intcode[self.pointer]
        func, num_params = self.opcode_map[opcode]
        params = self.intcode[self.pointer+1: self.pointer+num_params+1]
        func(params)
        
    def run(self):
        while self.pointer <= len(self.intcode):
            try:
                self.run_iteration()
            except StopIteration:
                break
        return self.intcode
