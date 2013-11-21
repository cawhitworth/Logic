from Sim.gates import AND, OR, NOT, XOR
from Sim.sim import Wire, HIGH, LOW

class SR:
    def __init__(self, S, R, Q, notQ, simulation, monitor=None):
        internalWire1 = Wire("", monitor)
        internalWire2 = Wire("", monitor)

        or1 = OR(R, notQ, internalWire1, simulation)
        not1 = NOT(internalWire1, Q, simulation)
        or2 = OR(S, Q, internalWire2, simulation)
        not2 = NOT(internalWire2, notQ, simulation)

class D:
    def __init__(self, D, E, Q, notQ, simulation, monitor=None):
        S = Wire("", monitor)
        R = Wire("", monitor)
        notD = Wire("", monitor)

        inv = NOT(D, notD, simulation)
        and1 = AND(notD, E, R, simulation)
        and2 = AND(D, E, S, simulation)

        sr = SR(S, R, Q, notQ, simulation, monitor)
