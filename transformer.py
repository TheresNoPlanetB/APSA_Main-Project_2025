import numpy as np
from bus import Bus

class Transformer:
    """
    The Transformer class models a transformer in a power system.
    Transformers connect two buses with specific parameters such as power rating, impedance, and X/R ratio.
    """

    def __init__(self, name: str, bus1: Bus, bus2: Bus, power_rating: float, impedance_percent: float,
                 x_over_r_ratio: float, base_mva: float, connection_type: str = "Y-Y", zg1: float = 0.0, zg2: float = 0.0):
        """
        Initialize the Transformer object with the given parameters.

        :param name: Name of the transformer
        :param bus1: The first bus connected by the transformer
        :param bus2: The second bus connected by the transformer
        :param power_rating: Power rating of the transformer (in MVA)
        :param impedance_percent: Impedance of the transformer (in percent)
        :param x_over_r_ratio: X/R ratio of the transformer
        """
        self.name = name  # Name of the transformer
        self.bus1 = bus1  # The first bus connected by the transformer
        self.bus2 = bus2  # The second bus connected by the transformer
        self.power_rating = power_rating  # Power rating of the transformer
        self.impedance_percent = impedance_percent  # Impedance of the transformer (in percent)
        self.x_over_r_ratio = x_over_r_ratio  # X/R ratio of the transformer
        self.base_mva = base_mva  # Base MVA for per-unit calculations
        self.connection_type = connection_type.upper()
        self.zg1 = zg1 # Grounding impedance on bus1 side (0 = solid, None = ungrounded)
        self.zg2 = zg2 # Grounding impedance on bus2 side

        self.s_base = 100

        # Calculate impedance and admittance values
        self.calc_impedance()
        self.calc_admittance()

        # Store Yprim matrices for each sequence
        self.yprim_sequences = {
            'positive': self.calc_yprim(sequence = 'positive'),
            'negative': self.calc_yprim(sequence = 'negative'),
            'zero': self.calc_yprim(sequence = 'zero'),
        }

    def calc_impedance(self):
        """
        Calculate the impedance (zt) of the transformer.
        """

        # Transformer impedance percentage
        z_pu = (self.impedance_percent / 100) * (self.s_base / self.power_rating)

        # Actual transformer impedance (zt)
        zt = z_pu

        # Calculate reactance using X/R ratio
        self.reactance = zt / np.sqrt(1 + (1 / self.x_over_r_ratio) ** 2)

        # Calculate resistance
        self.resistance = self.reactance / self.x_over_r_ratio if self.x_over_r_ratio != 0 else 0  # avoids division by 0

        # Calculate total impedance
        self.zt = np.round(complex(self.resistance, self.reactance), 6)

    def calc_admittance(self):
        """
        Calculate the admittance (yt) of the transformer.
        """
        # Admittance is the reciprocal of impedance
        if self.zt != 0:
            self.yt = 1 / self.zt
        else:
            self.yt = complex(0, 0)

    def calc_yprim(self, sequence = 'positive'):
        """
        Calculate the primitive admittance matrix (Yprim) for a specific sequence.
        Handles ungrounded Y connections in zero sequence.

        :param sequence: 'positive', 'negative', or 'zero'
        :return: 2x2 numpy array
        """
        y_series = self.yt

        if sequence in ['positive', 'negative']:
            return np.array([
                [y_series, -y_series],
                [-y_series, y_series]
            ])

        elif sequence == 'zero':
            y11 = y22 = y12 = y21 = 0

            if 'Y' in self.connection_type:
                if self.connection_type.startswith('Y'):
                    if self.zg1 is not None and self.zg1 > 0:
                        y11 += 1 / (1j * self.zg1)
                if self.connection_type.endswith('Y'):
                    if self.zg2 is not None and self.zg2 > 0:
                        y22 += 1 / (1j * self.zg2)

            # Include series branch if both sides are grounded or at least one
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
        """
        Retrieve Yprim for a given sequence.
        """
        return self.yprim_sequences.get(sequence, self.yprim_sequences['positive'])

    def __str__(self):
        """
        Return a string representation of the Transformer object.
        """
        return f"Transformer(name={self.name}, bus1={self.bus1}, bus2={self.bus2}, power_rating={self.power_rating}, impedance_percent={self.impedance_percent}, x_over_r_ratio={self.x_over_r_ratio})"

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
