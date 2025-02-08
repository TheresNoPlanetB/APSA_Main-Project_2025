import numpy as np
class TransmissionLine:
    """
    The TransmissionLine class models a transmission line connecting two buses in a power system.
    This class uses the Conductor and Geometry subclasses to determine its electrical characteristics.
    """

    def __init__(self, name, bus1, bus2, bundle, geometry, length):
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
        self.length = length  # Length of the transmission line
        self.f = 60
        self.S_Base = 100
        self.calc_base_values() # calculate base values
        self.calc_admittances()  # calculate admittances
        self.calc_yprim()  # calculate yprim



    def calc_base_values(self):
        """
        Calculate base impedance and admittance values for the transmission line.
        """

        # Placeholder for base impedance calculation (zbase)
        self.zbase = self.bus1.base_kv**2/self.S_Base  # Replace with actual calculation

        # Placeholder for base admittance calculation (ybase)
        self.ybase = 1/self.zbase  # Replace with actual calculation



    def calc_admittances(self):
        """
        Calculate series impedance, shunt admittance, and series admittance for the transmission line.
        """

        # Placeholder for series reactance calculation (xseries)
        self.xseries = (2 * np.pi * self.f) * (2 * 10 ** (-7)) * np.log(self.geometry.Deq / self.bundle.DSL)# Replace with actual calculation

        #calculate per unit xseries
        self.xseries_pu = self.xseries/self.zbase

        # Placeholder for series resistance calculation (rseries)
        self.rseries = self.bundle.conductor.resistance / self.bundle.num_conductors

        #calculate per unit rseries
        self.rseries_pu = self.rseries/self.zbase

        # Placeholder for series impedance calculation (zseries)
        self.zseries = complex(self.rseries, self.xseries)

        #calculate per unit zseries
        self.zseries_pu = self.zseries/self.zbase

        # Placeholder for shunt admittance calculation (yshunt)
        self.yshunt = 2 * np.pi * self.f * (2 * np.pi * 8.854 * 10 ** -12) / (np.log(self.geometry.Deq / self.bundle.DSC)) * 1609.34  # Replace with actual calculation

        # calculate per unit yshunt
        self.yshunt_pu = self.yshunt / self.ybase

        # Calculate series admittance
        self.yseries = 1 / self.zseries if self.zseries != 0 else complex(0, 0)

        # calculate per unit yshunt
        self.yseries_pu = self.yseries / self.ybase

    def calc_yprim(self):
        """
        Calculate and populate the admittance matrix (yprim) for the transmission line.
        """
        # Placeholder for admittance matrix calculation (yprim)
        self.yprim_pu = np.array([[self.yseries_pu + self.yshunt_pu/2, -1/self.yseries_pu],[-1/(self.yseries_pu), self.yseries_pu + self.yshunt_pu/2]])  # Replace with actual calculation



    def __str__(self):
        """
        Return a string representation of the TransmissionLine object.
        """
        return f"TransmissionLine(name={self.name}, bus1={self.bus1}, bus2={self.bus2}, length={self.length})"

if __name__ == '__main__':

    from Bus import Bus
    from Geometry import Geometry
    from Bundle import Bundle
    from Conductor import Conductor
    from TransmissionLine import TransmissionLine

    bus1 = Bus("Bus 1", 20)
    bus2 = Bus("Bus 2", 230)
    conductor1 = Conductor("conductor1", 5, 6, 8, 10)
    bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
    geometry1 = Geometry("Geometry 1", 5, 10, 18.5, 15, 37, 20)
    line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, 10)
    print(f"Name:{line1.name}, Bus1 Name:{line1.bus1.name}, Bus2 Name:{line1.bus2.name}, Length:{line1.length}")
    print(f"Base Impedance: zbase = {line1.zbase}")
    print(f"Base Admittance: ybase = {line1.ybase}")
    print(f"Series Impedance per Unit: zseries_pu = {line1.zseries_pu}")
    print(f"Series Resistance per Unit: rseries_pu = {line1.rseries_pu}")
    print(f"Series Reactance per Unit: xseries_pu = {line1.xseries_pu}")
    print(f"Equivalent Distance per phase: Deq = {line1.geometry.Deq}")

    print(f"Shunt Admittance per Unit: yshunt_pu = {line1.yshunt_pu}")
    print(f"Series Admittance per Unit: yseries_pu = {line1.yseries_pu}")
    print(f"Admittance Matrix per Unit: yprim_pu = {line1.yprim_pu}")




