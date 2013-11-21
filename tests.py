import Sim.sim as sim
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
        wire = components.Wire()
        notifyClient = LogicTests.NotifyClient()
        wire.connect(notifyClient)
        wire.setState(components.HIGH)
        self.assertEqual(notifyClient.notified, True)

    def testInverterDoesAnInvert(self):
        inputWire = components.Wire()
        outputWire = components.Wire()
        queue = LogicTests.MockEventQueue()
        sim = LogicTests.MockSimulation()
        inverter = components.NOT(inputWire, outputWire, sim)
        inputWire.setState(components.HIGH)
        self.assertEqual(outputWire.state, components.LOW)

    def testAndOfTwoHighGivesHigh(self):
        inputA = components.Wire()
        inputB = components.Wire()
        outputWire = components.Wire()
        queue = LogicTests.MockEventQueue()
        sim = LogicTests.MockSimulation()
        ander = components.AND(inputA, inputB, outputWire, sim)
        inputA.setState(components.HIGH)
        inputB.setState(components.HIGH)
        self.assertEqual(outputWire.state, components.HIGH)

    def testAndOfAnythingElseGivesLow(self):
        inputA = components.Wire()
        inputB = components.Wire()
        outputWire = components.Wire()
        queue = LogicTests.MockEventQueue()
        sim = LogicTests.MockSimulation()
        ander = components.AND(inputA, inputB, outputWire, sim)
        outputs = []
        inputA.setState(components.LOW)
        inputB.setState(components.HIGH)
        outputs.append(outputWire.state)

        inputB.setState(components.LOW)
        outputs.append(outputWire.state)

        inputA.setState(components.HIGH)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [components.LOW] * 3)

    def testOrOfTwoLowsGivesLow(self):
        inputA = components.Wire()
        inputB = components.Wire()
        outputWire = components.Wire()
        queue = LogicTests.MockEventQueue()
        sim = LogicTests.MockSimulation()
        orer = components.OR(inputA, inputB, outputWire, sim)
        inputA.setState(components.LOW)
        inputB.setState(components.LOW)
        self.assertEqual(outputWire.state, components.LOW)

    def testOrOfAnythingElseGivesHigh(self):
        inputA = components.Wire()
        inputB = components.Wire()
        outputWire = components.Wire()
        queue = LogicTests.MockEventQueue()
        sim = LogicTests.MockSimulation()
        orer = components.OR(inputA, inputB, outputWire, sim)
        outputs = []
        inputA.setState(components.LOW)
        inputB.setState(components.HIGH)
        outputs.append(outputWire.state)

        inputA.setState(components.HIGH)
        outputs.append(outputWire.state)

        inputB.setState(components.LOW)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [components.HIGH] * 3)

    def testXorOneWireHighGivesHigh(self):
        inputA = components.Wire()
        inputB = components.Wire()
        outputWire = components.Wire()
        queue = LogicTests.MockEventQueue()
        sim = LogicTests.MockSimulation()
        orer = components.XOR(inputA, inputB, outputWire, sim)
        outputs = []
        inputA.setState(components.LOW)
        inputB.setState(components.HIGH)
        outputs.append(outputWire.state)

        inputA.setState(components.HIGH)
        inputB.setState(components.LOW)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [components.HIGH] * 2)

    def testXorTwoWiresHighOrLowGivesLow(self):
        inputA = components.Wire()
        inputB = components.Wire()
        outputWire = components.Wire()
        queue = LogicTests.MockEventQueue()
        sim = LogicTests.MockSimulation()
        orer = components.XOR(inputA, inputB, outputWire, sim)
        outputs = []
        inputA.setState(components.LOW)
        inputB.setState(components.LOW)
        outputs.append(outputWire.state)

        inputA.setState(components.HIGH)
        inputB.setState(components.HIGH)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [components.LOW] * 2)

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

        inputWire = components.Wire()
        outputWire = components.Wire()

        inverter = components.NOT(inputWire, outputWire, simulation)

        takeInputWireHigh = sim.TimedEvent(0,
            lambda : inputWire.setState(components.HIGH))

        eventQueue.insertAt(takeInputWireHigh)

        simulation.runUntilComplete()

        self.assertEqual(outputWire.state, components.LOW)

    def testSimulateInverterTime(self):
        eventQueue = sim.EventQueue()
        simulation = sim.Simulation(eventQueue)
        monitor = SimulationTests.Monitor(simulation)

        inputWire = components.Wire("",monitor)
        outputWire = components.Wire("",monitor)

        inverter = components.NOT(inputWire, outputWire, simulation)

        simulation.addActionAfter(lambda : inputWire.setState(components.HIGH), 0)

        simulation.runUntilComplete()

        self.assertEqual(monitor.alerts[1], (1, outputWire, components.LOW))

if __name__ == "__main__":
    unittest.main()
