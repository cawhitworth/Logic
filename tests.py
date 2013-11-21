import Sim.sim as sim
import Sim.gates as gates
import Sim.components as components
import unittest

class LogicTests(unittest.TestCase):
    class NotifyClient:
        def __init__(self):
            self.notified = False

        def notify(self, wire):
            self.notified = True

    class MockEventQueue:
        def __init__(self):
            pass

        def insertAt(self, event):
            event.event()

    class MockSimulation:
        def now(self):
            return 0

        def addActionAfter(self,action, delay):
            action()

    def testWireNotifiesOnStateChanges(self):
        wire = sim.Wire()
        notifyClient = LogicTests.NotifyClient()
        wire.connect(notifyClient)
        wire.setState(sim.HIGH)
        self.assertEqual(notifyClient.notified, True)

    def testInverterDoesAnInvert(self):
        inputWire = sim.Wire()
        outputWire = sim.Wire()
        queue = LogicTests.MockEventQueue()
        simulator = LogicTests.MockSimulation()
        inverter = gates.NOT(inputWire, outputWire, simulator)
        inputWire.setState(sim.HIGH)
        self.assertEqual(outputWire.state, sim.LOW)

    def testAndOfTwoHighGivesHigh(self):
        inputA = sim.Wire()
        inputB = sim.Wire()
        outputWire = sim.Wire()
        queue = LogicTests.MockEventQueue()
        simulator = LogicTests.MockSimulation()
        ander = gates.AND(inputA, inputB, outputWire, simulator)
        inputA.setState(sim.HIGH)
        inputB.setState(sim.HIGH)
        self.assertEqual(outputWire.state, sim.HIGH)

    def testAndOfAnythingElseGivesLow(self):
        inputA = sim.Wire()
        inputB = sim.Wire()
        outputWire = sim.Wire()
        queue = LogicTests.MockEventQueue()
        simulator = LogicTests.MockSimulation()
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
        queue = LogicTests.MockEventQueue()
        simulator = LogicTests.MockSimulation()
        orer = gates.OR(inputA, inputB, outputWire, simulator)
        inputA.setState(sim.LOW)
        inputB.setState(sim.LOW)
        self.assertEqual(outputWire.state, sim.LOW)

    def testOrOfAnythingElseGivesHigh(self):
        inputA = sim.Wire()
        inputB = sim.Wire()
        outputWire = sim.Wire()
        queue = LogicTests.MockEventQueue()
        simulator = LogicTests.MockSimulation()
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
        queue = LogicTests.MockEventQueue()
        simulator = LogicTests.MockSimulation()
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
        queue = LogicTests.MockEventQueue()
        simulator = LogicTests.MockSimulation()
        orer = gates.XOR(inputA, inputB, outputWire, simulator)
        outputs = []
        inputA.setState(sim.LOW)
        inputB.setState(sim.LOW)
        outputs.append(outputWire.state)

        inputA.setState(sim.HIGH)
        inputB.setState(sim.HIGH)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [sim.LOW] * 2)

class QueueTests(unittest.TestCase):
    def testEmptyQueueIsEmpty(self):
        queue = sim.EventQueue()
        self.assertEqual(len(queue.queue), 0)

    def testInsertSingleItem(self):
        queue = sim.EventQueue()
        event = sim.TimedEvent(0, "Hello")
        queue.insertAt( event )
        self.assertEqual(queue.pop(), event)

    def testSequentialInserts(self):
        queue = sim.EventQueue()
        e1 = sim.TimedEvent(0, "Hello")
        e2 = sim.TimedEvent(1, "Goodbye")
        queue.insertAt(e1)
        queue.insertAt(e2)
        self.assertEqual(queue.pop(), e1)

    def testNonSequentialInserts(self):
        queue = sim.EventQueue()
        e1 = sim.TimedEvent(0, "Hello")
        e2 = sim.TimedEvent(1, "Goodbye")
        queue.insertAt(e2)
        queue.insertAt(e1)
        self.assertEqual(queue.pop(), e1)

    def testNonSequentialInserts2(self):
        queue = sim.EventQueue()
        e1 = sim.TimedEvent(0, "Hello")
        e2 = sim.TimedEvent(1, "Goodbye")
        e3 = sim.TimedEvent(2, "Back again")
        queue.insertAt(e2)
        queue.insertAt(e3)
        queue.insertAt(e1)
        (r1, r2, r3) = (queue.pop(), queue.pop(), queue.pop())
        self.assertEqual( (r1, r2, r3), (e1, e2, e3) )

class SimulationTests(unittest.TestCase):
    class Monitor:
        def __init__(self, simulation):
            self.alerts = []
            self.simulation = simulation

        def addWire(self, name):
            pass

        def notify(self, wire):
            self.alerts.append( (self.simulation.now(), wire, wire.state) )

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
        monitor = SimulationTests.Monitor(simulation)

        inputWire = sim.Wire("",monitor)
        outputWire = sim.Wire("",monitor)

        inverter = gates.NOT(inputWire, outputWire, simulation)

        simulation.addActionAfter(lambda : inputWire.setState(sim.HIGH), 0)

        simulation.runUntilComplete()

        self.assertEqual(monitor.alerts[1], (1, outputWire, sim.LOW))

class ComponentTests(unittest.TestCase):
    def testClock(self):
        eq = sim.EventQueue()
        s = sim.Simulation(eq)
        monitor = SimulationTests.Monitor(s)

        wire = sim.Wire("", monitor)

        clk = components.Clock(wire, 50, 50, s)

        s.runStep()
        s.runStep()
        s.runStep()

        self.assertEqual(monitor.alerts[1:],
            [ (50, wire, sim.HIGH),
              (100, wire, sim.LOW) ] )



if __name__ == "__main__":
    unittest.main()
