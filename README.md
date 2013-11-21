# Logic

This is a simple event-based logic simulator in Python.

The sample circuits should give an idea of how to use it.

## Setting up a simulation

```
from Sim.sim import EventQueue, Simulation
eq = EventQueue()
sim = Simulation(eq)
```

## Wires

Create a wire:

```
from Sim.sim import Wire
w = Wire("wireName", monitor)
w.connect(component) # generally, wires are passed into components who
                     # connect themselves, rather than doing this.
```

Both constructor parameters are optional. A name will be automatically
generated if one is not supplied (or if the name is an empty string).

A `Wire` will `notify` any `connect`ed components, passing itself in as the
parameter, as well as its `monitor` if one is supplied.

Use `monitor`s to watch circuit behaviour.

## Components

All components have the general form:

`Component(inputWire1, inputWire2, ... , outputWire1, outputWire2, ..., [parameters], simulation)`

### Basic gates

These are in `Sim.gates`

`AND`, `OR`, `NOT` and `XOR` gates are available.

### General components

These are in `Sim.components.components`.

`Clock(outputWire, tHigh, tLow, sim)` - provides a simple oscillator that takes
`outputWire` high after `tHigh` ticks and low after `tLow` ticks

### Maths

These are in `Sim.components.maths`

There's a `HalfAdder` and `FullAdder` that operate pretty much as you'd expect.

### Latches

These are in `Sim.components.latches`

An `SR`-latch and `D`-latch are available.

## Tests

There are Python unit tests in `tests/`. Running `tests.py` will run them.
