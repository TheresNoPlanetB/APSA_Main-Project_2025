from bus import Bus
import numpy as np

class Generator:
    """
    The generator class models power injections.
    It includes base conversion to system base MVA.
    """
    def __init__(self, name: str, bus: Bus, voltage_setpoint: float, mw_setpoint: float,
                 x1_pu: float, x2_pu: float, x0_pu: float, base_mva: float,
                 x1pp_pu: float = None, x2pp_pu: float = None, x0pp_pu: float = None,
                 grounding_r_pu: float = 0.0, grounding_x_pu: float = 0.0,
                 grounded: bool = True, system_base_mva: float = 100.0):

        self.name = name
        self.bus = bus
        self.voltage_setpoint = voltage_setpoint
        self.mw_setpoint = mw_setpoint
        self.base_mva = base_mva
        self.system_base_mva = system_base_mva
        self.grounded = grounded

        # Convert reactances to system base
        conversion_ratio = system_base_mva / base_mva

        # Sequence reactances (converted to system base)
        self.x1_pu = x1_pu * conversion_ratio
        self.x2_pu = x2_pu * conversion_ratio
        self.x0_pu = x0_pu * conversion_ratio

        # Subtransient reactances
        self.x1pp_pu = x1pp_pu * conversion_ratio if x1pp_pu else self.x1_pu
        self.x2pp_pu = x2pp_pu * conversion_ratio if x2pp_pu else self.x2_pu
        self.x0pp_pu = x0pp_pu * conversion_ratio if x0pp_pu else self.x0_pu

        # Grounding impedance p.u.
        self.grounding_z_pu = complex(grounding_r_pu, grounding_x_pu)

    def get_subtransient_reactance(self, sequence: str) -> float:
        """
        Returns subtransient reactance for the given sequence.
        """
        if sequence == 'positive':
            return self.x1pp_pu
        elif sequence == 'negative':
            return self.x2pp_pu
        elif sequence == 'zero':
            if self.grounded:
                return self.x0pp_pu + self.grounding_z_pu.imag
            else:
                return self.x0pp_pu # No grounding reactance added
        else:
            raise ValueError("Invalid sequence type")

    def calc_yprim(self, sequence='positive'):
        """
        Calculates the generator's admittance matrix for a given sequence.
        Used for fault analysis.
        """
        x = self.get_subtransient_reactance(sequence)
        if x == 0:
            raise ZeroDivisionError(f"Reactance for {sequence} sequence is zero for generator {self.name}.")

        y = 1 / (1j * x)
        return np.array([[y, -y], [-y, y]])


if __name__ == '__main__':
    from bus import Bus

    buses = [
        Bus("Bus 7", 50, "PV Bus")
    ]

    generators = [
        Generator("Gen1", buses[0], 230, 145),
    ]

    for generator in generators:
        bus = generator.bus
        print(
            f"Name: {generator.name}, Bus: {bus.name}, Voltage: {bus.base_kv}V, " 
            f"Voltage Setpoint: {generator.voltage_setpoint}V, MW Setpoint: {generator.mw_setpoint}MW")