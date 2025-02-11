class Bundle:
    def __init__(self, name, num_conductors, spacing, conductor):
        self.name = name #assign name of bundle
        self.num_conductors = num_conductors #assign number of conductors in bundle
        self.spacing = spacing #assign spacing between conductors
        self.conductor = conductor #assign name of conductor
        self.diameter = self.conductor.diam #Define conductor Diameter
        self.radius = self.diameter / 2 #Define conductor Radius
        self.calc_DSC() #calculate and assign value DSC
        self.calc_DSL() #calculate and assign value DSL


    def calc_DSL(self):
        if self.num_conductors == 1:
            # if 1 conductor bundle, DSL = GMR
            self.DSL = self.conductor.GMR
        if self.num_conductors == 2:
            # if 2 conductor bundle, DSL = (GMR*diam)^0.5
            self.DSL = (self.conductor.GMR * self.diameter)**0.5
        if self.num_conductors == 3:
            # if 3 conductor bundle, DSL = (GMR*diam^2)^(1/3)
            self.DSL = (self.conductor.GMR * self.diameter**2)**(1/3)
        if self.num_conductors == 4:
            # if 4 conductor bundle, DSL = 1.091 * (GMR*diam^3)^(1/4)
            self.DSL = 1.091 * (self.conductor.GMR * self.diameter**3)**(1/4)

    def calc_DSC(self):
        if self.num_conductors == 1:
            # if 1 conductor bundle, DSC = radius
            self.DSC = self.radius
        if self.num_conductors == 2:
            # if 2 conductor bundle, DSC = (radius*diam)^0.5
            self.DSC = (self.radius * self.diameter)**0.5
        if self.num_conductors == 3:
            # if 3 conductor bundle, DSC = (radius*diam^2)^(1/3)
            self.DSC = (self.radius * self.diameter**2)**(1/3)
        if self.num_conductors == 4:
            # if 4 conductor bundle, DSL = 1.091 * (radius*diam^3)^(1/4)
            self.DSC = 1.091 * (self.radius * self.diameter**3)**(1/4)

if __name__ == '__main__':
    from Bundle import Bundle
    from Conductor import Conductor

    conductor1 = Conductor("conductor1", 5, 6, 8, 10)
    bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
    print(
        f"Name:{bundle1.name}, Diam:{bundle1.num_conductors}, Spacing:{bundle1.spacing}, Conductor:{bundle1.conductor.name}")
    print(f"DSC:{bundle1.DSC}, DSL:{bundle1.DSL}")




