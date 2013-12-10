from Sim.gates import AND, OR, NOT, XOR
from Sim.sim import Wire, HIGH, LOW

class Clock:
    def __init__(self, out, tHigh, tLow, sim):
        self.out = out
        self.tHigh = tHigh
        self.tLow = tLow
        self.sim = sim

        sim.addActionAfter( lambda : out.setState(LOW), 0)
        sim.addActionAfter(self.clock, tLow)

    def clock(self):
        if self.out.state == LOW:
            self.out.setState(HIGH)
            self.sim.addActionAfter(self.clock, self.tHigh)
        else:
            self.out.setState(LOW)
            self.sim.addActionAfter(self.clock, self.tLow)

class Buffer:
    def __init__(self, I, O, sim):
        I.connect(self)
        self.O = O
        self.sim = sim

    def notify(self, wire):
        futureState = wire.state
        action = lambda : self.outputWire.setState(futureState)
        self.sim.addActionAfter(action, 1, self.O)

class BusBuffer:
    def __init__(self, I, O, sim):
        if len(I) != len(O):
            raise ValueError("Input and output buses must be same width")
        self.O = {}
        self.sim = sim
        for wire in range(len(I)):
            I[wire].connect(self)
            self.O[ I[wire] ] = O[wire]

    def notify(self, wire):
        futureState = wire.state
        action = lambda : self.O[wire].setState(futureState)
        self.sim.addActionAfter(action, 1, self.O[wire])


