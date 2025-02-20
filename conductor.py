class Conductor:
    """
    The Conductor class models the physical and electrical characteristics of a conductor used in transmission lines.
    """

    def __init__(self, name, diam, GMR, resistance, ampacity):
        """
        Initialize the Conductor object with the given parameters.

        :param name: Name of the conductor
        :param diam: Diameter of the conductor (in inches)
        :param GMR: Geometric Mean Radius (in feet)
        :param resistance: Resistance of the conductor (in ohms per mile)
        :param ampacity: Ampacity of the conductor (in amperes)
        """
        self.name = name  # Name of the conductor
        self.diam = diam  # Diameter of the conductor
        self.GMR = GMR  # Geometric Mean Radius of the conductor
        self.resistance = resistance  # Electrical resistance of the conductor
        self.ampacity = ampacity  # Maximum current carrying capacity of the conductor


    def __str__(self):
        """
        Return a string representation of the Conductor object.
        """
        return f"Conductor(name={self.name}, diam={self.diam}, GMR={self.GMR}, resistance={self.resistance}, ampacity={self.ampacity})"

#test
if __name__ == '__main__':
    from conductor import Conductor

    conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    print(
        f"Name:{conductor1.name}, Diam:{conductor1.diam}, GMR:{conductor1.GMR}, resistance:{conductor1.resistance}, ampacity:{conductor1.ampacity}")



