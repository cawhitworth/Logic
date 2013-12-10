from Sim.components import registers
from Sim.components import maths
from Sim.components import components
from Sim.components import flipflops
from Sim.sim import Wire, Bus, EventQueue, Simulation, LOW, HIGH
from Sim.monitor import LiveMonitor

eq = EventQueue()
s = Simulation(eq)
m = LiveMonitor(s)

CLK = Wire("CLK")
clk = components.Clock(CLK, 100, 100, s)

A = Bus(8, "A")
B = Bus(8, "B")
S = Bus(8, "S")

CIN = Wire("CIN")
COUT = Wire("COUT")
CIN_ = CIN # TODO latch
COUT_ = COUT # TODO latch

A_ = Bus(8, "A_")
B_ = Bus(8, "B_")
S_ = Bus(8, "S_")

factory = flipflops.FastStable.Factory

regA = registers.R(A, A_, CLK, s, factory)
regB = registers.R(B, B_, CLK, s, factory)
regS = registers.R(S_, S, CLK, s, factory)

adder = maths.BusAdder(A_, B_, CIN_, S_, COUT_, s)

A.write(20)
B.write(30)
CIN.setState(LOW)

print("Running until second falling edge...")
s.runUntil(390)
print("Ready now..")

s.runUntil(1000)

print(S.read())
