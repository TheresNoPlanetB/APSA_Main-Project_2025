from Bus import Bus
from Geometry import Geometry
from Bundle import Bundle
from Conductor import Conductor
from TransmissionLine import TransmissionLine

bus1 = Bus("Bus 1", 20)
bus2 = Bus("Bus 2", 230)
conductor1 = Conductor("conductor1", 5, 6, 8, 10)
bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)
line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, 10)
print(f"Name:{line1.name}, Bus1 Name:{line1.bus1.name}, Bus2 Name:{line1.bus2.name}, Length:{line1.length}")
print(f"zbase:{line1.zbase}, ybase:{line1.ybase}")
print(f"zseries:{line1.zseries}, yshunt:{line1.yshunt}, yseries:{line1.yseries}")
print(f"yprim:{line1.yprim}")


