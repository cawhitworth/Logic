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

class Inverter:
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



