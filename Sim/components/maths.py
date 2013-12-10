from Sim.gates import AND, OR, NOT, XOR
from Sim.sim import Wire, HIGH, LOW

class HalfAdder:
    def __init__(self, a, b, s, c, simulation):
        self.sumCalc = XOR(a, b, s, simulation)
        self.carryCalc = AND(a, b, c, simulation)

class FullAdder:
    def __init__(self, a, b, cIn, s, cOut, simulation, monitor=None):
        ha1Sum = Wire("", monitor)
        ha1Carry = Wire("", monitor)
        ha2Carry = Wire("", monitor)

        self.ha1 = HalfAdder(a, b, ha1Sum, ha1Carry, simulation)
        self.ha2 = HalfAdder(cIn, ha1Sum, s, ha2Carry, simulation)
        self.carry = OR(ha1Carry, ha2Carry, cOut, simulation)

class BusAdder:
    def __init__(self, A, B, CIN, S, COUT, simulation, monitor = None):
        if len(A) != len(B):
            raise ValueError("Input buses must be of equal width")
        if len(A) != len(S):
            raise ValueError("Output bus must be same width as input")

        width = len(A)

        carryWire = CIN
        carryOut = None
        for i in range(width):
            if i < width - 1:
                carryOut = Wire("", monitor)
            else:
                carryOut = COUT
            adder = FullAdder(A[i], B[i], carryWire, S[i], carryOut, simulation, monitor)
            carryWire = carryOut

