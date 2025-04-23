import numpy as np
from bus import Bus

class Transformer:
    """
    The Transformer class models a transformer in a power system,
    including grounding and connection types for sequence network modeling.
    """

    def __init__(self, name: str, bus1: Bus, bus2: Bus, power_rating: float, impedance_percent: float,
                 x_over_r_ratio: float, base_mva: float, connection_type: str = "Y-Y",
                 zg1: float = None, zg2: float = None):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio
        self.base_mva = base_mva
        self.connection_type = connection_type.upper()
        self.zg1 = zg1  # Grounding impedance on bus1 side (None = ungrounded, 0 = solid)
        self.zg2 = zg2

        self.s_base = 100  # System base MVA

        self.calc_impedance()
        self.calc_admittance()

        self.yprim_sequences = {
            'positive': self.calc_yprim('positive'),
            'negative': self.calc_yprim('negative'),
            'zero': self.calc_yprim('zero'),
        }

        if self.zg1 is not None:
            self.zg1 *= self.s_base / self.base_mva

    def calc_impedance(self):
        z_pu = (self.impedance_percent / 100) * (self.s_base / self.power_rating)
        zt = z_pu
        self.reactance = zt / np.sqrt(1 + (1 / self.x_over_r_ratio) ** 2)
        self.resistance = self.reactance / self.x_over_r_ratio if self.x_over_r_ratio != 0 else 0
        self.zt = np.round(complex(self.resistance, self.reactance), 6)

    def calc_admittance(self):
        self.yt = 1 / self.zt if self.zt != 0 else complex(0, 0)

    def calc_yprim(self, sequence='positive'):
        y_series = self.yt

        if sequence in ['positive', 'negative']:
            return np.array([
                [y_series, -y_series],
                [-y_series, y_series]
            ])

        elif sequence == 'zero':
            y11 = y22 = y12 = y21 = 0

            side1, side2 = self.connection_type.split('-')

            if side1 == 'Y':
                if self.zg1 is None:
                    y11 = 0
                elif self.zg1 == 0:
                    y11 += complex(0, 1e6)  # solid ground = high admittance
                else:
                    y11 += 1 / (1j * self.zg1)

            if side2 == 'Y':
                if self.zg2 is None:
                    y22 = 0
                elif self.zg2 == 0:
                    y22 += complex(0, 1e6)
                else:
                    y22 += 1 / (1j * self.zg2)

            if y11 != 0 or y22 != 0:
                y11 += y_series
                y22 += y_series
                y12 = y21 = -y_series

            return np.array([
                [y11, y12],
                [y21, y22]
            ])

        else:
            raise ValueError(f"Unknown sequence type: {sequence}")

    def get_yprim(self, sequence='positive'):
        return self.yprim_sequences.get(sequence, self.yprim_sequences['positive'])

    def __str__(self):
        return (f"Transformer(name={self.name}, bus1={self.bus1}, bus2={self.bus2}, "
                f"power_rating={self.power_rating}, impedance_percent={self.impedance_percent}, "
                f"x_over_r_ratio={self.x_over_r_ratio}, connection_type={self.connection_type})")

# Testing
if __name__ == '__main__':

    from bus import Bus

    bus1 = Bus("Bus 1", 20, "Slack Bus")
    bus2 = Bus("Bus 2", 230,"PQ Bus")
    transformer1 = Transformer("T1", bus1, bus2, 125, 8.5, 10, 100)
    print(f"Name: {transformer1.name}, Connection 1: {transformer1.bus1.name}, Bus Connection 2: {transformer1.bus2.name}, impedance_percent: {transformer1.impedance_percent}, x_over_r_ratio: {transformer1.x_over_r_ratio}")
    print(f"Impedance (per unit): {transformer1.zt}, Admittance (per unit): {transformer1.yt}")
    print(f"Y-Prim matrix:\n{transformer1.yprim}")

    bus6 = Bus("Bus 6", 230, "PQ Bus")
    bus7 = Bus("Bus 7", 18, "PQ Bus")
    transformer2 = Transformer("T2", bus6, bus7, 200, 10.5, 12, 100)
    print(f"Name: {transformer2.name}, Connection 1: {transformer2.bus1.name}, Bus Connection 2: {transformer2.bus2.name}, impedance_percent: {transformer2.impedance_percent}, x_over_r_ratio: {transformer2.x_over_r_ratio}")
    print(f"Impedance (per unit): {transformer2.zt}, Admittance (per unit): {transformer2.yt}")
    print(f"Y-Prim matrix:\n{transformer2.yprim}")
