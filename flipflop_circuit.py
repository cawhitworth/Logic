from Sim.components import flipflops
from Sim.components import components
from Sim.sim import Wire, EventQueue, Simulation, LOW, HIGH
from Sim.monitor import LiveMonitor

eq = EventQueue()
s = Simulation(eq)
m = LiveMonitor(s)

D = Wire("D", m)
CLK = Wire("CLK", m)
Q = Wire("Q", m)
notQ = Wire("~Q")

clk = components.Clock(CLK, 50, 50, s)

ff = flipflops.D_MS_FET(D, CLK, Q, notQ, s)

s.addActionAfter(lambda : D.setState(LOW), 75, D)
s.addActionAfter(lambda : D.setState(HIGH), 125, D)
s.addActionAfter(lambda : D.setState(LOW), 145, D)
s.addActionAfter(lambda : D.setState(HIGH), 175, D)

m.notifying = False

# Everything will be invalid until falling clock edge - Q
# will oscillate wildly
s.runUntil(90)
m.notifying = True

s.runUntil(125)
s.runUntil(225) # Q will go high shortly after t = 200

