class LoggingMonitor:
    def __init__(self, simulation):
        self.wires = []
        self.alerts = []
        self.simulation = simulation

    def addWire(self, wire):
        self.wires.append(wire.name)

    def notify(self, wire):
        self.alerts.append( (self.simulation.now(), wire, wire.state) )

    def reset(self):
        self.alerts = []

    def log(self):
        for alert in self.alerts:
            (time, wire, state) = alert
            print("{0} : {1} -> {2}".format(time, wire.name, state))

class LiveMonitor:
    def __init__(self, simulation):
        self.wires = []
        self.alerts = []
        self.simulation = simulation

    def addWire(self, wire):
        pass

    def notify(self, wire):
        print("{0} : {1} -> {2}".format(self.simulation.now(), wire.name, wire.state))

    def reset(self):
        self.alerts = []
