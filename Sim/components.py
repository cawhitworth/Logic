import Sim.sim

FLOATING = -1
LOW = 0
HIGH = 1

class Wire:
    def __init__(self):
        self.state = FLOATING
        self.connections = []

    def connect(self, component):
        self.connections.append(component)

    def setState(self, state):
        if self.state != state:
            self.state = state
            for connection in self.connections:
                connection.notify()

class NOT:
    def __init__(self, inputWire, outputWire, eventQueue):
        self.outputWire = outputWire
        self.inputWire = inputWire
        self.eventQueue = eventQueue
        inputWire.connect(self)

    def notify(self):
        futureState = HIGH if self.inputWire.state == LOW else LOW

        event = Sim.sim.TimedEvent(self.eventQueue.now() + 1,
            lambda : self.outputWire.setState(futureState))

        self.eventQueue.insertAt(event)

class AND:
    def __init__(self, inputWireA, inputWireB, outputWire, eventQueue):
        self.inputWireA = inputWireA
        self.inputWireB = inputWireB
        self.outputWire = outputWire
        self.eventQueue = eventQueue
        inputWireA.connect(self)
        inputWireB.connect(self)

    def notify(self):
        futureState = LOW
        if self.inputWireA.state == HIGH and self.inputWireB.state == HIGH:
           futureState = HIGH

        event = Sim.sim.TimedEvent(self.eventQueue.now() + 1,
            lambda : self.outputWire.setState(futureState))

        self.eventQueue.insertAt(event)

