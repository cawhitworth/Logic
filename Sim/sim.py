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
            indices = find_indices(self.queue, lambda t : t.time < evt.time)
            if len(indices) > 0:
                self.queue.insert(indices[-1]+1, evt)
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
            evt = self.eventQueue.pop()
            self.t = evt.time
            evt.event()

    def now(self):
        return self.t
