import numpy as np
class Transformer:
    """
    The Transformer class models a transformer in a power system.
    Transformers connect two buses with specific parameters such as power rating, impedance, and X/R ratio.
    """

    def __init__(self, name, bus1, bus2, power_rating, impedance_percent, x_over_r_ratio):
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
<<<<<<< HEAD
=======
        self.base_mva = 100
        self.v1 = v1
        self.v2 = v2
>>>>>>> parent of f64c03a (Update transformer.py)

        # Calculate impedance and admittance values
        self.calc_impedance()
        self.calc_admittance()
        self.calc_yprim()

    def calc_impedance(self):
        """
        Calculate the impedance (zt) of the transformer.
        """
<<<<<<< HEAD
        # Convert impedance from percent to per unit
        z_base = (self.impedance_percent / 100) * (self.power_rating / 100)

        # Calculate resistance and reactance based on X/R ratio
        self.resistance = z_base / (1 + self.x_over_r_ratio ** 2) ** 0.5
        self.reactance = self.resistance * self.x_over_r_ratio
=======
        # Compute base impedance z_base using the tranformer's voltage and power rating
        z_base_sys = ((self.bus1.base_kv * 1e3) ** 2) / (self.base_mva * 1e6) # Ohms
        z_base_xf = ((self.v1 * 1e3) ** 2) / (self.power_rating * 1e6)


        # Convert percentage impedance to per unit impedance
        z_pu = (self.impedance_percent / 100) * (z_base_xf / z_base_sys)

        # Calculate the actual transformer impedance (zt)
        zt = z_pu

        # Calculate reactance using X/R ratio

        self.reactance = zt / np.sqrt(1 + (1 / self.x_over_r_ratio) ** 2)

        # Calculate resistance
        self.resistance = self.reactance / self.x_over_r_ratio if self.x_over_r_ratio != 0 else 0 # avoids division by 0
>>>>>>> parent of f64c03a (Update transformer.py)

        # Calculate total impedance
        self.zt = complex(self.resistance, self.reactance)


    def calc_admittance(self):
        """
        Calculate the admittance (yt) of the transformer.
        """
        # Admittance is the reciprocal of impedance
        if self.zt != 0:
            self.yt = 1 / self.zt
        else:
            self.yt = complex(0, 0)

    def calc_yprim(self):
        """
        Calculate and populate the admittance matrix (yprim) for the transformer.
        """
        # Calculate the series admittance (inverse of series impedance)
        y_series = self.yt

        # Form the admittance matrix
        self.yprim = np.array([
            [y_series, -y_series],
            [-y_series, y_series]
        ])

    def __str__(self):
        """
        Return a string representation of the Transformer object.
        """
        return (f"Transformer(name={self.name}, bus1={self.bus1}, bus2={self.bus2}, power_rating={self.power_rating}, impedance_percent={self.impedance_percent}, x_over_r_ratio={self.x_over_r_ratio})")


#Testing
if __name__ == '__main__':
    #import Transformer from transformer
    from bus import Bus

    bus1 = Bus("Bus 1", 20)
    bus2 = Bus("Bus 2", 230)
<<<<<<< HEAD
    transformer1 = Transformer("T1", bus1, bus2, 125, 8.5, 10)
    print(f"Name:{transformer1.name}, Bus1 name:{transformer1.bus1.name}, Bus2 name:{transformer1.bus2.name}, power rating:{transformer1.power_rating}, impedance_percent:{transformer1.impedance_percent}, x_over_r_ratio:{transformer1.x_over_r_ratio}")
    print(f"impedance{transformer1.zt}, admittance{transformer1.yt}")
    print(f" matrix validation:{transformer1.yprim}")

=======
    transformer1 = Transformer("T1", bus1, bus2, 100, 8.5, 10, 100, 230, 230)
    print(f"Name:{transformer1.name}, Bus1 name:{transformer1.bus1.name}, Bus2 name:{transformer1.bus2.name}, power rating:{transformer1.power_rating}, impedance_percent:{transformer1.impedance_percent}, x_over_r_ratio:{transformer1.x_over_r_ratio}, MVA:{transformer1.base_mva}")
    print(f"impedance{transformer1.zt}, admittance{transformer1.yt}")
    print(f" matrix validation:{transformer1.yprim}")
>>>>>>> parent of f64c03a (Update transformer.py)
