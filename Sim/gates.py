from Sim.sim import FLOATING, LOW, HIGH

class NOT:
    def __init__(self, inputWire, outputWire, simulation):
        self.outputWire = outputWire
        self.inputWire = inputWire
        self.simulation = simulation
        inputWire.connect(self)

    def notify(self, wire):
        futureState = FLOATING
        if self.inputWire.state == HIGH:
            futureState = LOW
        if self.inputWire.state == LOW:
            futureState = HIGH

        action = lambda : self.outputWire.setState(futureState)
        self.simulation.addActionAfter(action, 1)

class AND:
    def __init__(self, inputWireA, inputWireB, outputWire, simulation):
        self.inputWireA = inputWireA
        self.inputWireB = inputWireB
        self.outputWire = outputWire
        self.simulation = simulation
        inputWireA.connect(self)
        inputWireB.connect(self)

    def notify(self, wire):
        futureState = FLOATING
        if self.inputWireA.state != FLOATING and self.inputWireB.state != FLOATING:
            if self.inputWireA.state == HIGH and self.inputWireB.state == HIGH:
               futureState = HIGH
            else:
               futureState = LOW

        action = lambda : self.outputWire.setState(futureState)
        self.simulation.addActionAfter(action, 1)

class OR:
    def __init__(self, inputWireA, inputWireB, outputWire, simulation):
        self.inputWireA = inputWireA
        self.inputWireB = inputWireB
        self.outputWire = outputWire
        self.simulation = simulation
        inputWireA.connect(self)
        inputWireB.connect(self)

    def notify(self, wire):
        futureState = FLOATING
        if self.inputWireA.state != FLOATING and self.inputWireB.state != FLOATING:
            if self.inputWireA.state != FLOATING and self.inputWireB.state != FLOATING:
                if self.inputWireA.state == HIGH or self.inputWireB.state == HIGH:
                   futureState = HIGH
                else:
                   futureState = LOW

        action = lambda : self.outputWire.setState(futureState)
        self.simulation.addActionAfter(action, 1)

class XOR:
    def __init__(self, inputWireA, inputWireB, outputWire, simulation):
        self.inputWireA = inputWireA
        self.inputWireB = inputWireB
        self.outputWire = outputWire
        self.simulation = simulation
        inputWireA.connect(self)
        inputWireB.connect(self)

    def notify(self, wire):
        futureState = FLOATING
        if self.inputWireA.state != FLOATING and self.inputWireB.state != FLOATING:
            if ((self.inputWireA.state == HIGH and self.inputWireB.state == LOW) or
                (self.inputWireA.state == LOW and self.inputWireB.state == HIGH)):
               futureState = HIGH
            else:
               futureState = LOW

        action = lambda : self.outputWire.setState(futureState)
        self.simulation.addActionAfter(action, 1)
