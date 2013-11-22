import Sim.sim as sim
import Sim.components.components as components
import Sim.components.mux as mux
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

    def test2to1Mux(self):
        eq = sim.EventQueue()
        s = sim.Simulation(eq)
        monitor = helpers.TestMonitor(s)

        X0 = sim.Wire("X0", monitor)
        X1 = sim.Wire("X1", monitor)
        C = sim.Wire("C", monitor)
        Z = sim.Wire("Z", monitor)

        m = mux.Mux2to1(X0, X1, C, Z, s)

        # Select X0, X0 = LOW
        X0.setState(sim.LOW)
        X1.setState(sim.LOW)
        C.setState(sim.LOW)
        s.runUntilComplete()

        # Select X0, X0 = HIGH
        X0.setState(sim.HIGH)
        s.runUntilComplete()

        # Select X0, X0 = LOW (ignore X1 = HIGH)
        X0.setState(sim.LOW)
        X1.setState(sim.HIGH)
        s.runUntilComplete()

        # Select X1, X1 = HIGH
        C.setState(sim.HIGH)
        s.runUntilComplete()

        # Select X1, X1 = LOW
        X1.setState(sim.LOW)
        s.runUntilComplete()

        # Ignore X0 - X1 = LOW (no transition, won't show)
        X0.setState(sim.HIGH)
        s.runUntilComplete()

        transitions = [ t[2] for t in monitor.alerts if t[1] == Z ]

        self.assertEqual( transitions, [ sim.LOW,
                                         sim.HIGH,
                                         sim.LOW,
                                         sim.HIGH,
                                         sim.LOW ])
