from Sim.sim import LOW, HIGH, EventQueue, Simulation, Wire
import Sim.gates as gates
from Sim.monitor import LoggingMonitor

class HalfAdder:
    def __init__(self, a, b, s, c, simulation):
        self.sumCalc = gates.XOR(a, b, s, simulation)
        self.carryCalc = gates.AND(a, b, c, simulation)

class FullAdder:
    def __init__(self, a, b, cIn, s, cOut, simulation, monitor):
        ha1Sum = Wire("", monitor)
        ha1Carry = Wire("", monitor)
        ha2Carry = Wire("", monitor)

        self.ha1 = HalfAdder(a, b, ha1Sum, ha1Carry, simulation)
        self.ha2 = HalfAdder(cIn, ha1Sum, s, ha2Carry, simulation)
        self.carry = gates.OR(ha1Carry, ha2Carry, cOut, simulation)

eq = EventQueue()
sim = Simulation(eq)
monitor = LoggingMonitor(sim)

a = Wire("a",monitor)
b = Wire("b",monitor)
cIn = Wire("cIn",monitor)
s = Wire("sum",monitor)
cOut = Wire("cOut",monitor)

fullAdder = FullAdder(a, b, cIn, s, cOut, sim, monitor)

a.setState(LOW)
b.setState(LOW)
cIn.setState(LOW)
sim.runUntilComplete()
monitor.log()
monitor.reset()
print()

a.setState(HIGH)
b.setState(HIGH)
sim.runUntilComplete()
monitor.log()
