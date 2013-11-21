from Sim.sim import LOW, HIGH, EventQueue, Simulation, Wire
from Sim.monitor import LiveMonitor
from Sim.components import latches

eq = EventQueue()
sim = Simulation(eq)
monitor = LiveMonitor(sim)

D = Wire("DATA", monitor)
E = Wire("ENA", monitor)
Q = Wire("Q", monitor)
notQ = Wire("~Q", monitor)

latch = latches.D(D, E, Q, notQ, sim)

D.setState(LOW)
E.setState(HIGH)
sim.runUntilComplete()
print("")

D.setState(HIGH)
sim.runUntilComplete()
print("")

E.setState(LOW)
sim.runUntilComplete()
print("")

D.setState(LOW)
sim.runUntilComplete()
print("")

E.setState(HIGH)
sim.runUntilComplete()
print("")

D.setState(HIGH)
sim.runUntilComplete()
D.setState(LOW)
sim.runUntilComplete()
