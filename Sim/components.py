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

class HalfAdder:
    def __init__(self, a, b, s, c, simulation):
        self.sumCalc = gates.XOR(a, b, s, simulation)
        self.carryCalc = gates.AND(a, b, c, simulation)

class FullAdder:
    def __init__(self, a, b, cIn, s, cOut, simulation, monitor=None):
        ha1Sum = Wire("", monitor)
        ha1Carry = Wire("", monitor)
        ha2Carry = Wire("", monitor)

        self.ha1 = HalfAdder(a, b, ha1Sum, ha1Carry, simulation)
        self.ha2 = HalfAdder(cIn, ha1Sum, s, ha2Carry, simulation)
        self.carry = gates.OR(ha1Carry, ha2Carry, cOut, simulation)
