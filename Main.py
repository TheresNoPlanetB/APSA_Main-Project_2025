from bus import Bus
from transformer import Transformer
from transmission_line import TransmissionLine
from bundle import Bundle
from geometry import Geometry
from circuit import Circuit

def main():
    # Create a Circuit instance
    circuit = Circuit("Test Circuit")

    # Add buses
    circuit.add_bus("Bus1", 20)
    circuit.add_bus("Bus2", 230)

    # Add a transformer
    circuit.add_transformer("T1", "Bus1", "Bus2", 125, 8.5, 10)

    # Add a transmission line
    conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
    geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)
    circuit.add_transmission_line("Line1", "Bus1", "Bus2", bundle1, geometry1, 10)

    # Print the circuit details
    print(circuit)

if __name__ == "__main__":
    main()