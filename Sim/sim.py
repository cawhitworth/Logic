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
            self.connect(monitor)

    def connect(self, component):
        self.connections.append(component)

    def setState(self, state):
        if self.state != state:
            self.state = state
            for connection in self.connections:
                connection.notify(self)

    def __repr__(self):
        return self.name

def find_indices(lst, condition):
    return [ i for (i, elem) in enumerate(lst) if condition(elem) ]

class TimedEvent:
    def __init__(self, time, event, key = None):
        self.time = time
        self.event = event
        self.key = key

    def __repr__(self):
        "{0}: {1} KEY {2}".format(self.time, self.event, self.key)

class EventQueue:
    def __init__(self):
        self.queue = []

    def insertAt(self, evt):

        # Zero length queue, just append it
        if len(self.queue) == 0:
            self.queue.append( evt )
        else:

            # if this is a keyed item, look for another item with the same
            # key at the same time and replace if necessary
            if evt.key != None:
                indices = find_indices(self.queue,
                    lambda t : evt.time == t.time and evt.key == t.key)

                if len(indices) > 0:
                    if len(indices) != 1:
                        raise "This shouldn't happen"
                    self.queue[indices[0]] = evt
                    return

            # otherwise, just insert it before the first element
            # with a greater time
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

    def runUntil(self, time):
        while self.eventQueue.len() > 0 and self.t < time:
            self.runStep()

    def runStep(self):
        evt = self.eventQueue.pop()
        self.t = evt.time
        evt.event()

    def addActionAfter(self, action, delay, key=None):
        evt = TimedEvent(self.now()+delay, action, key)
        self.eventQueue.insertAt(evt)

    def now(self):
        return self.t
