### Pauli class for operators and their methods ###

class Pauli:
    def __init__(self, phase, op):
        self.phase = phase
        self.op = op
    def __str__(self):
        return str(("Pauli", self.phase, self.op))
    __repr__ = __str__
    def __mul__(self, other):
        opa = self.op
        opb = other.op
        opc = ''
        n = len(opa)
        assert len(opa) == len(opb)
        phase = self.phase*other.phase
        for i in range(n):
            if opa[i] == 'I':
                opc += opb[i]
            elif opb[i] == 'I':
                opc += opa[i]
            elif opa[i] == opb[i]:
                opc += 'I'
                if opa[i] == 'Y':
                    phase *= -1
            elif (opa[i] == 'X' and opb[i] == 'Z'):
                opc += 'Y'
            elif (opa[i] == 'Z' and opb[i] == 'X'):
                opc += 'Y'
                phase *= -1
            elif (opa[i] == 'X' and opb[i] == 'Y'):
                opc += 'Z'
            elif (opa[i] == 'Y' and opb[i] == 'X'):
                opc += 'Z'
                phase *= -1    
            elif (opa[i] == 'Y' and opb[i] == 'Z'):
                opc += 'X'
            elif (opa[i] == 'Z' and opb[i] == 'Y'):
                opc += 'X'
                phase *= -1 
            else:
                assert 0
        return Pauli(phase, opc)
    def __neg__(self):
        return Pauli(-self.phase, self.op)
    def __eq__(self, other):
        return self.op == other.op and self.phase == other.phase
    def __ne__(self, other):
        return self.op != other.op or self.phase != other.phase
    def __hash__(self):
        return hash(str(self))
    def commutes(self, other):
        return self.__mul__(other) == other.__mul__(self)