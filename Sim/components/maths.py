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
