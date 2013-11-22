from Sim.components import latches
from Sim.gates import NOT
from Sim.sim import Wire

class D_MS_FET:
    def __init__(self, D, CLK, Q, notQ, simulation, monitor = None):
        notCLK = Wire("", monitor)
        intQ = Wire("", monitor)
        intNotQ = Wire("", monitor)

        inv = NOT(CLK, notCLK, simulation)
        latch1 = latches.D(D, CLK, intQ, intNotQ, simulation, monitor)
        latch2 = latches.D(intQ, notCLK, Q, notQ, simulation, monitor)

