import Sim.sim as sim
import Sim.components.components as components
import tests.helpers as helpers
import unittest

class ComponentTests(unittest.TestCase):
    def testClock(self):
        eq = sim.EventQueue()
        s = sim.Simulation(eq)
        monitor = helpers.TestMonitor(s)

        wire = sim.Wire("", monitor)

        clk = components.Clock(wire, 50, 50, s)

        s.runStep()
        s.runStep()
        s.runStep()

        self.assertEqual(monitor.alerts[1:],
            [ (50, wire, sim.HIGH),
              (100, wire, sim.LOW) ] )


