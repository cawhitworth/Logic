FLOATING = -1
LOW = 0
HIGH = 1

class Wire:
    instance = 0

    def __init__(self, name = "", monitor = None):
        self.state = FLOATING
        self.connections = []
        Wire.instance += 1
        if name == "":
            name = "Wire{0}".format(Wire.instance)
        self.name = name
        if monitor != None:
            self.connections.append(monitor)

    def connect(self, component):
        self.connections.append(component)

    def setState(self, state):
        if self.state != state:
            self.state = state
            for connection in self.connections:
                connection.notify(self)


def find_indices(lst, condition):
    return [ i for (i, elem) in enumerate(lst) if condition(elem) ]

class TimedEvent:
    def __init__(self, time, event):
        self.time = time
        self.event = event

    def __repr__(self):
        return "{0}: {1}".format(self.time, self.event)

class EventQueue:
    def __init__(self):
        self.queue = []

    def insertAt(self, evt):
        if len(self.queue) == 0:
            self.queue.append( evt )
        else:
            indices = find_indices(self.queue, lambda t : evt.time < t.time)
            if len(indices) > 0:
                self.queue.insert(indices[0], evt)
            else:
                self.queue.insert(len(self.queue)+1, evt)

    def next(self):
        return self.queue[0]

    def pop(self):
        return self.queue.pop(0)

    def len(self):
        return len(self.queue)

class Simulation:
    def __init__(self, eventQueue):
        self.eventQueue = eventQueue
        self.t = 0

    def runUntilComplete(self):
        while self.eventQueue.len() > 0:
            self.runStep()

    def runStep(self):
        evt = self.eventQueue.pop()
        self.t = evt.time
        evt.event()

    def addActionAfter(self, action, delay):
        evt = TimedEvent(self.now()+delay, action)
        self.eventQueue.insertAt(evt)

    def now(self):
        return self.t
