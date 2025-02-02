class Bundle:
    def __init__(self, name, num_conductors, spacing, conductor):
        self.name = name #assign name of bundle
        self.num_conductors = num_conductors #assign number of conductors in bundle
        self.spacing = spacing #assign spacing between conductors
        self.conductor = conductor #assign name of conductor
        self.calc_DSC() #calculate and assign value DSC
        self.calc_DSL() #calculate and assign value DSL

    def calc_DSC(self):
        self.DSC = None #Calculate and assign value DSC

    def calc_DSL(self):
        self.DSL = None #Calculate and assign value DSL





