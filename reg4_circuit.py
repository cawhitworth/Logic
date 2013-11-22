from Sim.components import registers
from Sim.components import components
from Sim.sim import Bus, Wire, EventQueue, Simulation, LOW, HIGH
from Sim.monitor import LiveMonitor

eq = EventQueue()
s = Simulation(eq)
m = LiveMonitor(s)

IN = Bus(4, "IN")
OUT = Bus(4, "OUT")
CLK = Wire("CLK")
clk = components.Clock(CLK, 50, 50, s)

reg = registers.R4_FET(IN, OUT, CLK, s)

for i in range(4):
    IN[i].setState(LOW)

# Bus is undefined until t = 100 (clock falling edge)

s.runUntil(125)

print( OUT.read()) # 0

IN[3].setState(HIGH)
IN[1].setState(HIGH)
s.runUntil(175)

print( OUT.read()) # 0

s.runUntil(225)

print( OUT.read()) # 2_1010
