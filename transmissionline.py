import numpy as np
from bus import Bus
from bundle import Bundle
from geometry import Geometry

class TransmissionLine:
    """
    The TransmissionLine class models a transmission line connecting two buses in a power system.
    This class uses the Conductor and Geometry subclasses to determine its electrical characteristics.
    """

    def __init__(self, name: str, bus1: Bus, bus2: Bus, bundle: Bundle, geometry: Geometry, length: float):
        """
        Initialize the TransmissionLine object with the given parameters.

        :param name: Name of the transmission line
        :param bus1: The first bus connected by the transmission line
        :param bus2: The second bus connected by the transmission line
        :param bundle: The bundle of conductors used in the transmission line
        :param geometry: The physical arrangement of conductors in the transmission line
        :param length: Length of the transmission line (in miles)
        """

        self.name = name  # Name of the transmission line
        self.bus1 = bus1  # The first bus connected by the transmission line
        self.bus2 = bus2  # The second bus connected by the transmission line
        self.bundle = bundle  # The bundle of conductors used in the transmission line
        self.geometry = geometry  # The physical arrangement of conductors in the transmission line
        self.length = length  # Length of the transmission line in miles
        self.f = 60
        self.S_Base = 100

        self.zbase = self.calc_base_values()
        self.ybase = 1 / self.zbase  # Replace with actual calculation

        self.zseries = None
        self.zseries_pu = None
        self.rseries = None
        self.rseries_pu = None
        self.xseries = None
        self.xseries_pu = None
        self.yseries = None
        self.yseries_pu = None
        self.yshunt = None
        self.yshunt_pu = None
        self.yprim_pu = None

        self.calc_base_values()  # calculate base values
        self.calc_admittances()  # calculate admittances
        self.calc_yprim()  # calculate yprim

        # Calculate sequence impedances and admittances
        self.calc_sequence_impedances()
        self.calc_sequence_admittances()
        self.calc_all_yprim_sequences()

    def calc_base_values(self):
        """
        Calculate base impedance and admittance values for the transmission line.
        """

        # Base impedance calculation (zbase)
        return self.bus1.base_kv**2/self.S_Base  # Replace with actual calculation

    def calc_admittances(self):
        """
        Calculate series impedance, shunt admittance, and series admittance for the transmission line.
        """

        # Placeholder for series reactance calculation (xseries)
        self.xseries = (2 * np.pi * self.f) * (2 * 10 ** (-7)) * np.log(self.geometry.Deq / self.bundle.DSL) * 1609.32 * self.length # Replace with actual calculation

        #calculate per unit xseries
        self.xseries_pu = self.xseries/self.zbase

        # Series resistance calculation (rseries)
        self.rseries = self.bundle.conductor.resistance / self.bundle.num_conductors * self.length

        #calculate per unit rseries
        self.rseries_pu = self.rseries/self.zbase

        #Series impedance calculation (zseries)
        self.zseries = complex(self.rseries, self.xseries)

        #Calculate per unit zseries
        self.zseries_pu = self.zseries/self.zbase

        # Shunt admittance calculation (yshunt)
        self.yshunt = (1j * 2 * np.pi * self.f) * ((2 * np.pi * 8.854 * 10 ** -12) / (np.log(self.geometry.Deq / self.bundle.DSC))) * 1609.34 * self.length

        # Calculate per unit yshunt
        self.yshunt_pu = self.yshunt / self.ybase

        # Calculate series admittance
        self.yseries = 1 / self.zseries if self.zseries != 0 else complex(0, 0)

        # calculate per unit yshunt
        self.yseries_pu = self.yseries / self.ybase

    def calc_yprim(self):
        """
        Calculate and populate the admittance matrix (yprim) for the transmission line.
        """
        # Admittance matrix calculation (yprim)
        self.yprim_pu = np.array([[self.yseries_pu + (self.yshunt_pu/2), -self.yseries_pu],[-self.yseries_pu, self.yseries_pu + (self.yshunt_pu/2)]])

    def calc_sequence_impedances(self):
        """Calculate sequence impedances in p.u."""
        # Series X from geometry (same for all sequences)
        x_series = (2 * np.pi * self.f) * (2e-7) * np.log(self.geometry.Deq / self.bundle.DSL)
        x_total = x_series * 1609.34 * self.length

        # Series R from bundle
        r_total = (self.bundle.conductor.resistance / self.bundle.num_conductors) * self.length

        # Positive and negative sequence impedance (identical for transposed)
        self.z1 = self.z2 = complex(r_total, x_total)

        # Zero-sequence impedance (estimated as 2.5R + jX)
        self.z0 = 2.5 * complex(r_total, x_total)

        # Convert to per-unit
        self.z1_pu = self.z1 / self.zbase
        self.z2_pu = self.z2 / self.zbase
        self.z0_pu = self.z0 / self.zbase

    def calc_sequence_admittances(self):
        """Compute series admittance for each sequence (Y = 1/Z)."""
        self.y1_pu = 1 / self.z1_pu if self.z1_pu != 0 else 0
        self.y2_pu = 1 / self.z2_pu if self.z2_pu != 0 else 0
        self.y0_pu = 1 / self.z0_pu if self.z0_pu != 0 else 0

    def calc_yprim_sequence(self, yseq):
        """Build a 2x2 Yprim matrix for a given sequence admittance."""
        return np.array([[yseq, -yseq], [-yseq, yseq]])

    def calc_all_yprim_sequences(self):
        """Generate Yprim matrices for all three sequence networks."""
        self.yprim_positive = self.calc_yprim_sequence(self.y1_pu)
        self.yprim_negative = self.calc_yprim_sequence(self.y2_pu)
        self.yprim_zero = self.calc_yprim_sequence(self.y0_pu)

    def get_yprim(self, sequence: str = 'positive'):
        """Return the Yprim matrix for the requested sequence."""
        if sequence == 'positive':
            return self.yprim_positive
        elif sequence == 'negative':
            return self.yprim_negative
        elif sequence == 'zero':
            return self.yprim_zero
        else:
            raise ValueError("Unknown sequence. Choose from 'positive', 'negative', 'zero'.")

    def __str__(self):
        """
        Return a string representation of the TransmissionLine object.
        """
        return f"TransmissionLine(name={self.name}, bus1={self.bus1}, bus2={self.bus2}, length={self.length} mi)"

if __name__ == '__main__':

    from bus import Bus
    from geometry import Geometry
    from bundle import Bundle
    from conductor import Conductor

    bus1 = Bus("Bus 2", 230, "PQ Bus")
    bus2 = Bus("Bus 4", 230, "PQ Bus")
    conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    bundle1 = Bundle("Bundle A", 2, 1.5, conductor1)
    geometry1 = Geometry("Geometry 1", 0, 0, 19.5, 0, 39, 0)
    line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, 10)
    #print(f"Name:{line1.name}, Bus1 Name:{line1.bus1.name}, Bus2 Name:{line1.bus2.name}, Length:{line1.length}")
    #print(f"Base Impedance: zbase = {line1.zbase}")
    #print(f"Base Admittance: ybase = {line1.ybase}")
    print(f"Series Impedance per Unit: zseries_pu = {line1.zseries_pu}")
    print(f"Series Resistance per Unit: rseries_pu = {line1.rseries_pu}")
    print(f"Series Reactance per Unit: xseries_pu = {line1.xseries_pu}")
    #print(f"Equivalent Distance per phase: Deq = {line1.geometry.Deq}")

    print(f"Shunt Admittance per Unit: yshunt_pu = {line1.yshunt_pu}")
    #print(f"Series Admittance per Unit: yseries_pu = {line1.yseries_pu}")
    #print(f"Admittance Matrix per Unit: yprim_pu = {line1.yprim_pu}")



