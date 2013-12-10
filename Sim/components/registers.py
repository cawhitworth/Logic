from Sim.components import flipflops
from Sim.sim import Bus

class R4_FET:
    def __init__(self, B_IN, B_OUT, CLK, sim):
        if len(B_IN) != 4:
            raise ValueError("4-bit register must have 4-bit input bus")
        if len(B_OUT) != 4:
            raise ValueError("4-bit register must have 4-bit output bus")

        B_OUTi = Bus(4)

        ffs = [ flipflops.D_MS_FET(B_IN[i], CLK, B_OUT[i], B_OUTi[i], sim)
                for i in range(4) ]

class R_FET:
    def __init__(self, B_IN, B_OUT, CLK, sim):
        if len(B_IN) != len(B_OUT):
            raise ValueError("Input and output buses must be equal width")

        width = len(B_IN)

        B_OUTi = Bus(width)

        ffs = [ flipflops.D_MS_FET(B_IN[i], CLK, B_OUT[i], B_OUTi[i], sim)
                for i in range(width) ]
