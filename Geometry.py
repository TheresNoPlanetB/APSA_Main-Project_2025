class Geometry:
    """
    The Geometry class models the physical arrangement of conductors in a transmission line.
    """

    def __init__(self, name, xa, ya, xb, yb, xc, yc):
        """
        Initialize the Geometry object with the given parameters.

        :param name: Name of the geometry
        :param xa: x-coordinate of conductor A
        :param ya: y-coordinate of conductor A
        :param xb: x-coordinate of conductor B
        :param yb: y-coordinate of conductor B
        :param xc: x-coordinate of conductor C
        :param yc: y-coordinate of conductor C
        """
        self.name = name  # Name of the geometry
        self.xa = xa  # x-coordinate of conductor A
        self.ya = ya  # y-coordinate of conductor A
        self.xb = xb  # x-coordinate of conductor B
        self.yb = yb  # y-coordinate of conductor B
        self.xc = xc  # x-coordinate of conductor C
        self.yc = yc  # y-coordinate of conductor C

        # Calculate the equivalent distance (Deq)
        self.calc_deq()

    def calc_deq(self):
        """
        Calculate the equivalent distance (Deq) for the geometry.
        """
        # Placeholder for Deq calculation
        Dab = abs((self.ya-self.yb)/(self.xa-self.xb))
        Dbc = abs((self.yb-self.yc)/(self.xb-self.xc))
        Dac = abs((self.ya-self.yc)/(self.xa-self.xc))

        self.Deq = (Dab * Dbc * Dac)**(1/3)  # Replace with actual calculation

    def __str__(self):
        """
        Return a string representation of the Geometry object.
        """
        return f"Geometry(name={self.name}, xa={self.xa}, ya={self.ya}, xb={self.xb}, yb={self.yb}, xc={self.xc}, yc={self.yc})"

if __name__ == '__main__':

    from Geometry import Geometry

    geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)
    print(f"Name:{geometry1.name}, xa:{geometry1.xa}, ya:{geometry1.ya}, xb:{geometry1.xb}, yb:{geometry1.yb}, xc:{geometry1.xc}, yc:{geometry1.yc}")
    print(f"Deq:{geometry1.Deq}")


