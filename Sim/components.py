import Sim.sim

FLOATING = -1
LOW = 0
HIGH = 1

class Wire:
    instance = 0

    def __init__(self, name = "", monitor = None):
        self.state = FLOATING
        self.connections = []
        self.monitor = monitor
        Wire.instance += 1
        if name == "":
            name = "Wire{0}".format(Wire.instance)
        self.name = name
        if monitor != None:
            monitor.addWire(self)

    def connect(self, component):
        self.connections.append(component)

    def setState(self, state):
        if self.state != state:
            if self.monitor is not None:
                self.monitor.alert(self, state)
            self.state = state
            for connection in self.connections:
                connection.notify()

class NOT:
    def __init__(self, inputWire, outputWire, eventQueue, simulation):
        self.outputWire = outputWire
        self.inputWire = inputWire
        self.eventQueue = eventQueue
        self.simulation = simulation
        inputWire.connect(self)

    def notify(self):
        futureState = FLOATING
        if self.inputWire.state == HIGH:
            futureState = LOW
        if self.inputWire.state == LOW:
            futureState = HIGH

        event = Sim.sim.TimedEvent(self.simulation.now() + 1,
            lambda : self.outputWire.setState(futureState))

        self.eventQueue.insertAt(event)

class AND:
    def __init__(self, inputWireA, inputWireB, outputWire, eventQueue, simulation):
        self.inputWireA = inputWireA
        self.inputWireB = inputWireB
        self.outputWire = outputWire
        self.eventQueue = eventQueue
        self.simulation = simulation
        inputWireA.connect(self)
        inputWireB.connect(self)

    def notify(self):
        futureState = FLOATING
        if self.inputWireA.state != FLOATING and self.inputWireB.state != FLOATING:
            if self.inputWireA.state == HIGH and self.inputWireB.state == HIGH:
               futureState = HIGH
            else:
               futureState = LOW

        event = Sim.sim.TimedEvent(self.simulation.now() + 1,
            lambda : self.outputWire.setState(futureState))

        self.eventQueue.insertAt(event)

class OR:
    def __init__(self, inputWireA, inputWireB, outputWire, eventQueue, simulation):
        self.inputWireA = inputWireA
        self.inputWireB = inputWireB
        self.outputWire = outputWire
        self.eventQueue = eventQueue
        self.simulation = simulation
        inputWireA.connect(self)
        inputWireB.connect(self)

    def notify(self):
        futureState = FLOATING
        if self.inputWireA.state != FLOATING and self.inputWireB.state != FLOATING:
            if self.inputWireA.state != FLOATING and self.inputWireB.state != FLOATING:
                if self.inputWireA.state == HIGH or self.inputWireB.state == HIGH:
                   futureState = HIGH
                else:
                   futureState = LOW

        event = Sim.sim.TimedEvent(self.simulation.now() + 1,
            lambda : self.outputWire.setState(futureState))

        self.eventQueue.insertAt(event)

class XOR:
    def __init__(self, inputWireA, inputWireB, outputWire, eventQueue, simulation):
        self.inputWireA = inputWireA
        self.inputWireB = inputWireB
        self.outputWire = outputWire
        self.eventQueue = eventQueue
        self.simulation = simulation
        inputWireA.connect(self)
        inputWireB.connect(self)

    def notify(self):
        futureState = FLOATING
        if self.inputWireA.state != FLOATING and self.inputWireB.state != FLOATING:
            if ((self.inputWireA.state == HIGH and self.inputWireB.state == LOW) or
                (self.inputWireA.state == LOW and self.inputWireB.state == HIGH)):
               futureState = HIGH
            else:
               futureState = LOW

        event = Sim.sim.TimedEvent(self.simulation.now() + 1,
            lambda : self.outputWire.setState(futureState))

        self.eventQueue.insertAt(event)
