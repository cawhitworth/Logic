from Sim.components import registers
from Sim.components import maths
from Sim.components import components
from Sim.components import flipflops
from Sim.components import components
from Sim.sim import Wire, Bus, EventQueue, Simulation, LOW, HIGH
from Sim.monitor import LiveMonitor

eq = EventQueue()
s = Simulation(eq)
m = LiveMonitor(s)

CLK = Wire("CLK")
clk = components.Clock(CLK, 100, 100, s)

ACC = Bus(8, "ACC",m)
ONE = Bus(8, "ONE",m)
R = Bus(8, "R")
CIN = Bus(1,"CIN")
COUT = Bus(1,"COUT")

ACC_ = Bus(8, "ACC_")
ONE_ = Bus(8, "ONE_")
R_ = Bus(8, "R_")
CIN_ = Bus(1,"CIN")
COUT_ = Bus(1,"COUT")

factory = flipflops.FastStable.Factory

regACC = registers.R(ACC, ACC_, CLK, s, factory)
regONE = registers.R(ONE, ONE_, CLK, s, factory)
regR   = registers.R(R_, R, CLK, s, factory)
regCIN = registers.R(CIN, CIN_, CLK, s, factory)
regCOUT = registers.R(COUT_, COUT, CLK, s, factory)

adder = maths.BusAdder(ACC_, ONE_, CIN_[0], R_, COUT_[0], s)

buff = components.BusBuffer(R, ACC, s)

CIN.write(0)
ONE.write(1)
ACC.write(0)

s.runUntil(5000)
print(ACC.read())
