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
CIN_ = Wire("CIN_")
COUT_ = Wire("COUT_")
tmp1 = Wire()
tmp2 = Wire()

A_ = Bus(8, "A_")
B_ = Bus(8, "B_")
S_ = Bus(8, "S_")

factory = flipflops.FastStable.Factory

regA = registers.R(A, A_, CLK, s, factory)
regB = registers.R(B, B_, CLK, s, factory)
regS = registers.R(S_, S, CLK, s, factory)
regCIN = flipflops.FastStable(CIN, CLK, CIN_, tmp1, s)
regCOUT = flipflops.FastStable(COUT, CLK, COUT_, tmp2, s)

adder = maths.BusAdder(A_, B_, CIN_, S_, COUT_, s)

A.write(20)
B.write(30)
CIN.setState(HIGH)

s.runUntil(250)
print(S.read())

s.runUntil(450)
print(S.read())

A.write(40)

s.runUntil(550)

print(S.read())

s.runUntil(650)

print(S.read())

A.write(10)

s.runUntil(750)

print(S.read())

s.runUntil(850)

print(S.read())

s.runUntil(1250)

print(S.read())
