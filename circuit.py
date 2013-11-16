import Sim.sim as s
import Sim.components as comp

class Monitor:
    def __init__(self, simulation):
        self.wires = {}
        self.alerts = []
        self.simulation = simulation

    def addWire(self, wire, name):
        self.wires[wire] = name

    def alert(self, wire, state):
        self.alerts.append( (self.simulation.now(), wire, state) )

    def reset(self):
        self.alerts = []

    def log(self):
        for alert in self.alerts:
            (time, wire, state) = alert
            print("{0} : {1} -> {2}".format(time, self.wires[wire], state))

class HalfAdder:
    def __init__(self, a, b, s, c, eventQueue, simulation):
        self.sumCalc = comp.XOR(a, b, s, eventQueue, simulation)
        self.carryCalc = comp.AND(a, b, c, eventQueue, simulation)

class FullAdder:
    def __init__(self, a, b, cIn, s, cOut, eventQueue, simulation):
        ha1Sum = comp.Wire()
        ha1Carry = comp.Wire()
        ha2Carry = comp.Wire()

        self.ha1 = HalfAdder(a, b, ha1Sum, ha1Carry, eventQueue, simulation)
        self.ha2 = HalfAdder(cIn, ha1Sum, s, ha2Carry, eventQueue, simulation)
        self.carry = comp.OR(ha1Carry, ha2Carry, cOut, eventQueue, simulation)

eq = s.EventQueue()
sim = s.Simulation(eq)
monitor = Monitor(sim)

a = comp.Wire(monitor)
b = comp.Wire(monitor)
cIn = comp.Wire(monitor)
s = comp.Wire(monitor)
cOut = comp.Wire(monitor)

monitor.addWire(a, "A")
monitor.addWire(b, "B")
monitor.addWire(cIn, "cIN")
monitor.addWire(s, "S")
monitor.addWire(cOut, "cOUT")

fullAdder = FullAdder(a, b, cIn, s, cOut, eq, sim)

a.setState(comp.LOW)
b.setState(comp.LOW)
cIn.setState(comp.LOW)
sim.runUntilComplete()
monitor.log()
monitor.reset()
print()

a.setState(comp.HIGH)
b.setState(comp.HIGH)
sim.runUntilComplete()
monitor.log()
