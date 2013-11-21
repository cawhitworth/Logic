from Sim.gates import AND, OR, NOT, XOR
from Sim.sim import Wire, HIGH, LOW

class Clock:
    def __init__(self, out, tHigh, tLow, simulation):
        self.out = out
        self.tHigh = tHigh
        self.tLow = tLow
        self.simulation = simulation

        simulation.addActionAfter( lambda : out.setState(LOW), 0)
        simulation.addActionAfter(self.clock, tLow)

    def clock(self):
        if self.out.state == LOW:
            self.out.setState(HIGH)
            self.simulation.addActionAfter(self.clock, self.tHigh)
        else:
            self.out.setState(LOW)
            self.simulation.addActionAfter(self.clock, self.tLow)

class SR:
    def __init__(self, S, R, Q, notQ, simulation, monitor=None):
        internalWire1 = Wire("", monitor)
        internalWire2 = Wire("", monitor)

        or1 = OR(R, notQ, internalWire1, simulation)
        not1 = NOT(internalWire1, Q, simulation)
        or2 = OR(S, Q, internalWire2, simulation)
        not2 = NOT(internalWire2, notQ, simulation)

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
