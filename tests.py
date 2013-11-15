import Sim.sim as sim
import Sim.components as components
import unittest

class LogicTests(unittest.TestCase):
    class NotifyClient:
        def __init__(self):
            self.notified = False

        def notify(self):
            self.notified = True

    class MockEventQueue:
        def __init__(self):
            pass

        def now(self):
            return 0

        def insertAt(self, event):
            event.event()

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
        inverter = components.NOT(inputWire, outputWire, queue)
        inputWire.setState(components.HIGH)
        self.assertEqual(outputWire.state, components.LOW)

    def testAndOfTwoHighGivesHigh(self):
        inputA = components.Wire()
        inputB = components.Wire()
        outputWire = components.Wire()
        queue = LogicTests.MockEventQueue()
        ander = components.AND(inputA, inputB, outputWire, queue)
        inputA.setState(components.HIGH)
        inputB.setState(components.HIGH)
        self.assertEqual(outputWire.state, components.HIGH)

    def testAndOfAnythingElseGivesLow(self):
        inputA = components.Wire()
        inputB = components.Wire()
        outputWire = components.Wire()
        queue = LogicTests.MockEventQueue()
        ander = components.AND(inputA, inputB, outputWire, queue)
        outputs = []
        inputA.setState(components.LOW)
        inputB.setState(components.HIGH)
        outputs.append(outputWire.state)

        inputB.setState(components.LOW)
        outputs.append(outputWire.state)

        inputA.setState(components.HIGH)
        outputs.append(outputWire.state)

        self.assertEqual(outputs, [components.LOW] * 3)


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


if __name__ == "__main__":
    unittest.main()
