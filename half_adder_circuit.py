import Sim.sim as s
import Sim.gates as gates
from Sim.monitor import LoggingMonitor

eq = s.EventQueue()
sim = s.Simulation(eq)
monitor = LoggingMonitor(sim)

a = s.Wire("a",monitor)
b = s.Wire("b",monitor)
orOut = s.Wire("orOut",monitor)
notOut = s.Wire("notOut",monitor)
sOut = s.Wire("s",monitor)
carry = s.Wire("carry",monitor)

or1 = gates.OR(a, b, orOut, sim)
and1 = gates.AND(a, b, carry, sim)
inv1 = gates.NOT(carry, notOut, sim)
and2 = gates.AND(orOut, notOut, sOut, sim)

a.setState(gates.HIGH)
b.setState(gates.HIGH)
sim.runUntilComplete()
monitor.log()
