from Sim.components import latches
from Sim.gates import NOT
from Sim.sim import Wire, HIGH, LOW, FLOATING, invert

class D_MS_FET:
    def __init__(self, D, CLK, Q, notQ, simulation, monitor = None):
        notCLK = Wire("", monitor)
        intQ = Wire("", monitor)
        intNotQ = Wire("", monitor)

        inv = NOT(CLK, notCLK, simulation)
        latch1 = latches.D(D, CLK, intQ, intNotQ, simulation, monitor)
        latch2 = latches.D(intQ, notCLK, Q, notQ, simulation, monitor)

    def Factory(D, CLK, Q, notQ, simulation, monitor = None):
        return D_MS_FET(D, CLK, Q, notQ, simulation, monitor)

class FastStable:
    def __init__(self, D, CLK, Q, notQ, sim, monitor = None):
        Q.setState(FLOATING)
        notQ.setState(FLOATING)
        CLK.connect(self)
        self.D = D
        self.Q = Q
        self.notQ = notQ
        self.sim = sim
        self.oldState = CLK.state

    def notify(self, wire):
        if wire.state == LOW and self.oldState == HIGH:
            qAction = lambda : self.Q.setState(self.D.state)
            notQAction = lambda : self.notQ.setState(invert(self.D.state))
            self.sim.addActionAfter(qAction, 1, self.Q)
            self.sim.addActionAfter(notQAction, 1, self.notQ)
        self.oldState = wire.state

    def Factory(D, CLK, Q, notQ, simulation, monitor = None):
        return FastStable(D, CLK, Q, notQ, simulation, monitor)
