from Bundle import Bundle
from Conductor import Conductor

conductor1 = Conductor("conductor1", 5, 6, 8, 10)
bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
print(f"Name:{bundle1.name}, Diam:{bundle1.num_conductors}, Spacing:{bundle1.spacing}, Conductor:{bundle1.conductor.name}")
print(f"DSC:{bundle1.DSC}, DSL:{bundle1.DSL}")



