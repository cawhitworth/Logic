from Sim.gates import AND, OR, NOT, XOR
from Sim.sim import Wire, HIGH, LOW

class Mux2to1:
    def __init__(self, X0, X1, C, Z, simulation, monitor = None):
        notC = Wire("", monitor)
        int1 = Wire("", monitor)
        int2 = Wire("", monitor)

        inv = NOT(C, notC, simulation)

        and1 = AND(X0, notC, int1, simulation)
        and2 = AND(X1, C, int2, simulation)
        or1 = OR(int1, int2, Z, simulation)

