import Sim.sim as sim
import unittest

class Tests(unittest.TestCase):
    def testEmptyQueueIsEmpty(self):
        queue = sim.EventQueue()
        self.assertEqual(len(queue.queue), 0)

    def testInsertSingleItem(self):
        queue = sim.EventQueue()
        event = sim.TimedEvent(0, "Hello")
        queue.insertAt( event )
        self.assertEqual(queue.next(), event)

    def testSequentialInserts(self):
        queue = sim.EventQueue()
        e1 = sim.TimedEvent(0, "Hello")
        e2 = sim.TimedEvent(1, "Goodbye")
        queue.insertAt(e1)
        queue.insertAt(e2)
        self.assertEqual(queue.next(), e1)


if __name__ == "__main__":
    unittest.main()
