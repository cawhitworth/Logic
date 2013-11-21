import Sim.sim as sim
import Sim.gates as gates
import tests.helpers as helpers
import unittest

class SimulationTests(unittest.TestCase):
    def testSimulateInverter(self):
        eventQueue = sim.EventQueue()
        simulation = sim.Simulation(eventQueue)

        inputWire = sim.Wire()
        outputWire = sim.Wire()

        inverter = gates.NOT(inputWire, outputWire, simulation)

        takeInputWireHigh = sim.TimedEvent(0,
            lambda : inputWire.setState(sim.HIGH))

        eventQueue.insertAt(takeInputWireHigh)

        simulation.runUntilComplete()

        self.assertEqual(outputWire.state, sim.LOW)

    def testSimulateInverterTime(self):
        eventQueue = sim.EventQueue()
        simulation = sim.Simulation(eventQueue)
        monitor = helpers.TestMonitor(simulation)

        inputWire = sim.Wire("",monitor)
        outputWire = sim.Wire("",monitor)

        inverter = gates.NOT(inputWire, outputWire, simulation)

        simulation.addActionAfter(lambda : inputWire.setState(sim.HIGH), 0)

        simulation.runUntilComplete()

        self.assertEqual(monitor.alerts[1], (1, outputWire, sim.LOW))
