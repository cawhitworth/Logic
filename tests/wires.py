import unittest
from Sim.sim import Wire, Bus

class WireTests(unittest.TestCase):
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
