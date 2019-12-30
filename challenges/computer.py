import functools


class Computer:
    def __init__(self, intcode, inputs):
        self.intcode = intcode.copy()
        self.inputs = inputs
        self.output = None
        self.outputs = []
        self.pointer = 0
        self.complete = False
        self.relative_base = 0

        self.opcode_map = {
            1: (self.opcode_1, 3),
            2: (self.opcode_2, 3),
            3: (self.opcode_3, 1),
            4: (self.opcode_4, 1),
            5: (self.opcode_5, 2),
            6: (self.opcode_6, 2),
            7: (self.opcode_7, 3),
            8: (self.opcode_8, 3),
            9: (self.opcode_9, 1),
            99: (self.opcode_99, 0)
        }

    def read_intcode(self, param, mode):
        try:
            if mode == 0:
                return self.intcode[param]
            elif mode == 1:
                return param
            elif mode == 2:
                loc = self.relative_base + param
                return self.intcode[loc]
            else:
                print("whoops", param, mode)
        except IndexError:
            return 0

    def write_intcode(self, param, value, mode):
        if mode == 0:
            position = param
        if mode == 1:
            position = param
        if mode == 2:
            position = param + self.relative_base
        try:
            self.intcode[position] = value
        except IndexError:
            self.intcode += [0] * (position + 1 - len(self.intcode))
            self.intcode[position] = value

    def revert_pointer_if_modified(self, func, params, modes):
        original_value_at_pointer = self.intcode[self.pointer]
        func_result = func(params, modes)
        if self.intcode[self.pointer] == original_value_at_pointer:
            self.pointer = func_result

    def opcode_1(self, params, modes):
        value_0 = self.read_intcode(params[0], modes[0])
        value_1 = self.read_intcode(params[1], modes[1])
        self.write_intcode(params[2], value_0 + value_1, modes[2])
        return self.pointer + len(params) + 1

    def opcode_2(self, params, modes):
        value_0 = self.read_intcode(params[0], modes[0])
        value_1 = self.read_intcode(params[1], modes[1])
        self.write_intcode(params[2], value_0 * value_1, modes[2])
        return self.pointer + len(params) + 1

    def opcode_3(self, params, modes):
        input_ = self.inputs.pop(0)
        self.write_intcode(params[0], input_, modes[0])
        return self.pointer + len(params) + 1

    def opcode_4(self, params, modes):
        val = self.read_intcode(params[0], modes[0])
        self.output = val
        self.outputs.append(val)
        return self.pointer + len(params) + 1

    def opcode_5(self, params, modes):
        value_0 = self.read_intcode(params[0], modes[0])
        value_1 = self.read_intcode(params[1], modes[1])
        result = value_1 if value_0 else self.pointer + len(params) + 1
        return result

    def opcode_6(self, params, modes):
        value_0 = self.read_intcode(params[0], modes[0])
        value_1 = self.read_intcode(params[1], modes[1])
        result = value_1 if not value_0 else self.pointer + len(params) + 1
        return result

    def opcode_7(self, params, modes):
        value_0 = self.read_intcode(params[0], modes[0])
        value_1 = self.read_intcode(params[1], modes[1])
        result = int(value_0 < value_1)
        self.write_intcode(params[2], result, modes[2])
        return self.pointer + len(params) + 1

    def opcode_8(self, params, modes):
        value_0 = self.read_intcode(params[0], modes[0])
        value_1 = self.read_intcode(params[1], modes[1])
        result = int(value_0 == value_1)
        self.write_intcode(params[2], result, modes[2])
        return self.pointer + len(params) + 1

    def opcode_9(self, params, modes):
        value = self.read_intcode(params[0], modes[0])
        self.relative_base += value
        return self.pointer + len(params) + 1

    def opcode_99(self, params, modes):
        raise StopIteration

    def func_and_modes(self, opcode):
        opcode = str(opcode)
        instruction = int(opcode.rjust(2, "0")[-2:])
        func, num_params = self.opcode_map[instruction]

        param_modes = opcode.rjust(num_params + 2, "0")
        param_modes = list((int(mode) for mode in param_modes))[:num_params]
        param_modes.reverse()
        param_modes = tuple(param_modes)
        return func, param_modes

    def run_iteration(self):
        opcode = self.intcode[self.pointer]
        func, modes = self.func_and_modes(opcode)
        params = self.intcode[self.pointer + 1: self.pointer + len(modes) + 1]
        self.revert_pointer_if_modified(func, params, modes)

    def run(self):
        while self.pointer <= len(self.intcode):
            try:
                self.run_iteration()
            except StopIteration:
                self.complete = True
                break
        return self
