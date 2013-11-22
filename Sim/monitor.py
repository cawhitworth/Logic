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
        self.simulation = simulation
        self.notifying = True

    def addWire(self, wire):
        pass

    def notify(self, wire):
        if self.notifying:
            print("{0} : {1} -> {2}".format(self.simulation.now(), wire.name, wire.state))

    def reset(self):
        pass

class CSVMonitor:
    def __init__(self, simulation):
        self.wires = []
        self.alerts = {}
        self.simulation = simulation
        self.recording = True

    def addWire(self, wire):
        self.wires.append(wire.name)

    def notify(self, wire):
        if self.notifying:
            now = self.simulation.now()
            if wire.name not in self.wires:
                self.wires.append(wire.name)
            if now in self.alerts.keys():

                self.alerts[now][wire.name] = wire.state
            else:
                self.alerts[now] = {}
                self.alerts[now][wire.name] = wire.state

    def write(self):
        output = []
        headers = ",".join( ['"{0}"'.format(w) for w in self.wires ] )
        output.append( '"time",{0}'.format(headers))
        for when in sorted(self.alerts.keys()):
            l = []
            alert = self.alerts[when]
            for wire in self.wires:
                wires = alert.keys()
                if wire in wires:
                    l.append('"{0}"'.format(alert[wire]))
                else:
                    l.append('""')
            line = '"{0}",{1}'.format(when, ",".join(l))
            output.append(line)

        return "\n".join(output)

