import Sim.sim as sim
import Sim.gates as gates
import Sim.components.components as components
import tests.helpers as helpers
import unittest

class LogicTests(unittest.TestCase):

    def testWireNotifiesOnStateChanges(self):
        wire = sim.Wire()
        notifyClient = helpers.MockNotifyClient()
        wire.connect(notifyClient)
        wire.setState(sim.HIGH)
        self.assertEqual(notifyClient.notified, True)

    def testInverterDoesAnInvert(self):
        inputWire = sim.Wire()
        outputWire = sim.Wire()
        queue = helpers.MockEventQueue()
        simulator = helpers.MockSimulation()
        inverter = gates.NOT(inputWire, outputWire, simulator)
        inputWire.setState(sim.HIGH)
        self.assertEqual(outputWire.state, sim.LOW)

    def testAndOfTwoHighGivesHigh(self):
        inputA = sim.Wire()
        inputB = sim.Wire()
        outputWire = sim.Wire()
        queue = helpers.MockEventQueue()
        simulator = helpers.MockSimulation()
        ander = gates.AND(inputA, inputB, outputWire, simulator)
        inputA.setState(sim.HIGH)
        inputB.setState(sim.HIGH)
        self.assertEqual(outputWire.state, sim.HIGH)

    def testAndOfAnythingElseGivesLow(self):
        inputA = sim.Wire()
        inputB = sim.Wire()
        outputWire = sim.Wire()
        queue = helpers.MockEventQueue()
        simulator = helpers.MockSimulation()
        ander = gates.AND(inputA, inputB, outputWire, simulator)
        outputs = []
        inputA.setState(sim.LOW)
        inputB.setState(sim.HIGH)
        outputs.append(outputWire.state)

        inputB.setState(sim.LOW)
        outputs.append(outputWire.state)

        inputA.setState(sim.HIGH)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [sim.LOW] * 3)

    def testOrOfTwoLowsGivesLow(self):
        inputA = sim.Wire()
        inputB = sim.Wire()
        outputWire = sim.Wire()
        queue = helpers.MockEventQueue()
        simulator = helpers.MockSimulation()
        orer = gates.OR(inputA, inputB, outputWire, simulator)
        inputA.setState(sim.LOW)
        inputB.setState(sim.LOW)
        self.assertEqual(outputWire.state, sim.LOW)

    def testOrOfAnythingElseGivesHigh(self):
        inputA = sim.Wire()
        inputB = sim.Wire()
        outputWire = sim.Wire()
        queue = helpers.MockEventQueue()
        simulator = helpers.MockSimulation()
        orer = gates.OR(inputA, inputB, outputWire, simulator)
        outputs = []
        inputA.setState(sim.LOW)
        inputB.setState(sim.HIGH)
        outputs.append(outputWire.state)

        inputA.setState(sim.HIGH)
        outputs.append(outputWire.state)

        inputB.setState(sim.LOW)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [sim.HIGH] * 3)

    def testXorOneWireHighGivesHigh(self):
        inputA = sim.Wire()
        inputB = sim.Wire()
        outputWire = sim.Wire()
        queue = helpers.MockEventQueue()
        simulator = helpers.MockSimulation()
        orer = gates.XOR(inputA, inputB, outputWire, simulator)
        outputs = []
        inputA.setState(sim.LOW)
        inputB.setState(sim.HIGH)
        outputs.append(outputWire.state)

        inputA.setState(sim.HIGH)
        inputB.setState(sim.LOW)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [sim.HIGH] * 2)

    def testXorTwoWiresHighOrLowGivesLow(self):
        inputA = sim.Wire()
        inputB = sim.Wire()
        outputWire = sim.Wire()
        queue = helpers.MockEventQueue()
        simulator = helpers.MockSimulation()
        orer = gates.XOR(inputA, inputB, outputWire, simulator)
        outputs = []
        inputA.setState(sim.LOW)
        inputB.setState(sim.LOW)
        outputs.append(outputWire.state)

        inputA.setState(sim.HIGH)
        inputB.setState(sim.HIGH)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [sim.LOW] * 2)
