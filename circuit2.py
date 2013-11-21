import Sim.sim as s
import Sim.components as comp
from Sim.monitor import LoggingMonitor

eq = s.EventQueue()
sim = s.Simulation(eq)
monitor = LoggingMonitor(sim)

a = comp.Wire("a",monitor)
b = comp.Wire("b",monitor)
orOut = comp.Wire("orOut",monitor)
notOut = comp.Wire("notOut",monitor)
s = comp.Wire("s",monitor)
carry = comp.Wire("carry",monitor)

or1 = comp.OR(a, b, orOut, sim)
and1 = comp.AND(a, b, carry, sim)
inv1 = comp.NOT(carry, notOut, sim)
and2 = comp.AND(orOut, notOut, s, sim)

a.setState(comp.HIGH)
b.setState(comp.HIGH)
sim.runUntilComplete()
monitor.log()
