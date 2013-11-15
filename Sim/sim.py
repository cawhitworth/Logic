FLOATING = -1
LOW = 0
HIGH = 1

class Wire:
    def __init__(self):
        self.state = FLOATING

def find_indices(lst, condition):
    return [ i for (i, elem) in enumerate(lst) if condition(elem) ]

class TimedEvent:
    def __init__(self, time, event):
        self.time = time
        self.event = event

class EventQueue:
    def __init__(self):
        self.queue = []

    def insertAt(self, evt):
        if len(self.queue) == 0:
            self.queue.append( evt )
        else:
            head, *tail = find_indices(self.queue, lambda t : t.time < evt.time)

    def next(self):
        return self.queue[0]
