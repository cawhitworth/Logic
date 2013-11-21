from Sim.sim import LOW, HIGH, EventQueue, Simulation, Wire
import Sim.gates as gates
from Sim.monitor import LoggingMonitor
from Sim.components.maths import FullAdder, HalfAdder

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
