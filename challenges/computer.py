import functools


class Computer:
    def __init__(self, intcode, inputs):
        self.intcode = intcode.copy()
        self.inputs = inputs
        self.outputs = []
        self.pointer = 0

        self.opcode_map = {
            1: (self.opcode_1, 3),
            2: (self.opcode_2, 3),
            3: (self.opcode_3, 1),
            4: (self.opcode_4, 1),
            5: (self.opcode_5, 2),
            6: (self.opcode_6, 2),
            7: (self.opcode_7, 3),
            8: (self.opcode_8, 3),
            99: (self.opcode_99, 0)
        }

    def get_value(self, param, mode):
        if not mode:
            return self.intcode[param]
        else:
            return param

    def get_values(self, params, modes):
        zipped = zip(params, modes)
        values = [self.get_value(*inputs) for inputs in zipped]
        return values

    def revert_pointer_if_modified(self, func, params, modes):
        original_value_at_pointer = self.intcode[self.pointer]
        func_result = func(params, modes)
        if self.intcode[self.pointer] == original_value_at_pointer:
            self.pointer = func_result

    def opcode_1(self, params, modes):
        values = self.get_values(params, modes)
        self.intcode[params[2]] = sum(values[:2])
        return self.pointer + len(params) + 1

    def opcode_2(self, params, modes):
        values = self.get_values(params, modes)
        self.intcode[params[2]] = values[0] * values[1]
        return self.pointer + len(params) + 1

    def opcode_3(self, params, _):
        input_ = self.inputs.pop(0)
        self.intcode[params[0]] = input_
        return self.pointer + len(params) + 1

    def opcode_4(self, params, modes):
        val = self.get_value(params[0], modes[0])
        self.outputs.append(val)
        return self.pointer + len(params) + 1

    def opcode_5(self, params, modes):
        values = self.get_values(params, modes)
        result = values[1] if values[0] else self.pointer + len(params) + 1
        return result

    def opcode_6(self, params, modes):
        values = self.get_values(params, modes)
        result = values[1] if not values[0] else self.pointer + len(params) + 1
        return result

    def opcode_7(self, params, modes):
        values = self.get_values(params, modes)
        result = int(values[0] < values[1])
        self.intcode[params[2]] = result
        return self.pointer + len(params) + 1

    def opcode_8(self, params, modes):
        values = self.get_values(params, modes)
        result = int(values[0] == values[1])
        self.intcode[params[2]] = result
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
                break
        return self
