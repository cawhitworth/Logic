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

class Buffer:
    def __init__(self, I, O, simulation):
        I.connect(self)
        self.O = O

    def notify(self, wire):
        futureState = wire.state
        action = lambda : self.outputWire.setState(futureState)
        self.simulation.addActionAfter(action, 1, self.O)



