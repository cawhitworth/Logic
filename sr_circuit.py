from Sim.sim import LOW, HIGH, EventQueue, Simulation, Wire
import Sim.gates as gates
from Sim.monitor import LiveMonitor
from Sim.components import latches

eq = EventQueue()
sim = Simulation(eq)
monitor = LiveMonitor(sim)

S = Wire("SET", monitor)
R = Wire("RESET", monitor)
Q = Wire("Q", monitor)
notQ = Wire("~Q", monitor)

latch = latches.SR(S, R, Q, notQ, sim)

S.setState(LOW)
R.setState(HIGH)
sim.runUntilComplete()
print("")
R.setState(LOW)
sim.runUntilComplete()
print("")
S.setState(HIGH)
sim.runUntilComplete()
print("")
S.setState(LOW)
sim.runUntilComplete()
print("")

#sim.addActionAfter( lambda : S.setState(HIGH), 1 )
#sim.addActionAfter( lambda : S.setState(LOW), 2 )
#sim.runUntilComplete()
#print()

#sim.addActionAfter( lambda : S.setState(HIGH), 1 )
#sim.addActionAfter( lambda : S.setState(LOW), 2 )
#sim.addActionAfter( lambda : S.setState(HIGH), 3 )


