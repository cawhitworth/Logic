import Sim.sim as sim
import unittest

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

    def testMultipleInsertsAtSameTimeWithDifferentKeysWorks(self):
        queue = sim.EventQueue()
        e1 = sim.TimedEvent(1, "Hello", "1")
        e2 = sim.TimedEvent(1, "Goodbye", "2")
        queue.insertAt(e1)
        queue.insertAt(e2)
        (r1, r2) = (queue.pop(), queue.pop())
        self.assertEqual( (r1, r2), (e1, e2) )

    def testMultipleInsertsAtSameTimeWithSameKeysWorks(self):
        queue = sim.EventQueue()
        e1 = sim.TimedEvent(1, "Hello", "1")
        e2 = sim.TimedEvent(1, "Goodbye", "1")
        queue.insertAt(e1)
        queue.insertAt(e2)
        self.assertEqual(queue.len(), 1)
        self.assertEqual(queue.pop(), e2)

