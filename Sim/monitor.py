class LoggingMonitor:
    def __init__(self, simulation):
        self.wires = []
        self.alerts = []
        self.simulation = simulation

    def addWire(self, wire):
        self.wires.append(wire.name)

    def alert(self, wire, state):
        self.alerts.append( (self.simulation.now(), wire, state) )

    def reset(self):
        self.alerts = []

    def log(self):
        for alert in self.alerts:
            (time, wire, state) = alert
            print("{0} : {1} -> {2}".format(time, wire.name, state))
