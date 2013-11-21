import Sim.sim as s
import Sim.components as comp
from Sim.monitor import LoggingMonitor

class HalfAdder:
    def __init__(self, a, b, s, c, eventQueue, simulation):
        self.sumCalc = comp.XOR(a, b, s, eventQueue, simulation)
        self.carryCalc = comp.AND(a, b, c, eventQueue, simulation)

class FullAdder:
    def __init__(self, a, b, cIn, s, cOut, eventQueue, simulation, monitor):
        ha1Sum = comp.Wire("", monitor)
        ha1Carry = comp.Wire("", monitor)
        ha2Carry = comp.Wire("", monitor)

        self.ha1 = HalfAdder(a, b, ha1Sum, ha1Carry, eventQueue, simulation)
        self.ha2 = HalfAdder(cIn, ha1Sum, s, ha2Carry, eventQueue, simulation)
        self.carry = comp.OR(ha1Carry, ha2Carry, cOut, eventQueue, simulation)

eq = s.EventQueue()
sim = s.Simulation(eq)
monitor = LoggingMonitor(sim)

a = comp.Wire("a",monitor)
b = comp.Wire("b",monitor)
cIn = comp.Wire("cIn",monitor)
s = comp.Wire("sum",monitor)
cOut = comp.Wire("cOut",monitor)

fullAdder = FullAdder(a, b, cIn, s, cOut, eq, sim, monitor)

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
