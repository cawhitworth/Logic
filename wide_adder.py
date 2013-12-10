from Sim.components import maths
from Sim.sim import Bus, Wire, EventQueue, Simulation, LOW, HIGH
from Sim.monitor import LiveMonitor


eq = EventQueue()
s = Simulation(eq)
m = LiveMonitor(s)

A = Bus(4, "A",)
B = Bus(4, "B",)
S = Bus(4, "S")
CIN = Wire("CIN")
COUT = Wire("COUT",m)

adder = maths.BusAdder(A, B, CIN, S, COUT, s)

CIN.setState(HIGH)

A.write(5)
B.write(6)

s.runUntilComplete()

print(S.read())
