class MockNotifyClient:
    def __init__(self):
        self.notified = False

    def notify(self, wire):
        self.notified = True

class MockEventQueue:
    def __init__(self):
        pass

    def insertAt(self, event):
        event.event()

class MockSimulation:
    def now(self):
        return 0

    def addActionAfter(self,action, delay, key=None):
        action()

class TestMonitor:
    def __init__(self, simulation):
        self.alerts = []
        self.simulation = simulation

    def addWire(self, name):
        pass

    def notify(self, wire):
        self.alerts.append( (self.simulation.now(), wire, wire.state) )
