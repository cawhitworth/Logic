import unittest
from Sim.sim import Wire, Bus, HIGH, LOW, FLOATING

class BusTests(unittest.TestCase):
    def testBusSize(self):
        b = Bus(2, "BUS")
        self.assertEqual(len(b), 2)

    def testBusNames(self):
        b = Bus(2, "BUS")
        names = [ w.name for w in b ]
        self.assertEqual(names, [ "BUS0", "BUS1" ])

    def testBusIndexing(self):
        b = Bus(4, "BUS")
        self.assertEqual("BUS2", b[2].name)

    def testDeletingFromBusFails(self):
        b = Bus(4, "BUS")
        def fn():
            del(b[1])
        self.assertRaises(TypeError, fn)

    def testAssigningToBusFails(self):
        b = Bus(4, "BUS")
        def fn():
            b[1] = Wire()
        self.assertRaises(TypeError, fn)

    def testAnonymousBuses(self):
        b = Bus(8)
        self.assertEqual(b[1].name, "{0}1".format(b.name))

    def testBusReadFloating(self):
        b = Bus(4)
        self.assertEqual(b.read(), FLOATING)

    def testBusRead(self):
        b = Bus(4)
        values = []
        for w in b: w.setState(LOW)
        values.append(b.read())
        b[0].setState(HIGH)
        values.append(b.read())
        b[1].setState(HIGH)
        values.append(b.read())
        b[2].setState(HIGH)
        values.append(b.read())
        b[3].setState(HIGH)
        values.append(b.read())
        self.assertEqual(values, [ 0, 1, 3, 7, 15 ] )
