#seeking to validate the project

from circuit import Circuit
from bus import Bus
from transformer import Transformer
from transmissionLine import TransmissionLine
from conductor import Conductor
from bundle import Bundle
from geometry import Geometry


# Step 1: Create a circuit
circuit1 = Circuit("Test Circuit: ⚡ validating...")

# Step 2: Check Attributes
print("Circuit Name:", circuit1.name)
print("Buses :", circuit1.buses)
print("Transformer Initialized:", circuit1.transformer)
print("Transmission Lines Initialized:", circuit1.transmission_line)

# Step 3: Add and retrieve equipment components

# Adding Buses
circuit1.add_bus("Bus1", 230)
circuit1.add_bus("Bus2", 115)

print("Buses in circuit:", list(circuit1.buses.keys()))

# Adding Transformer
circuit1.add_transformer("T1", "Bus1", "Bus2", 100, 8, 10, 100)

print("Transformers in circuit:", list(circuit1.transformer.keys()))

# Adding Transmission Line
conductor1 = Conductor("Conductor A", 0.642, 0.0217, 0.385, 460)
bundle1 = Bundle("Bundle A", 2, 1.5, conductor1)
geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)
circuit1.add_transmission_line("Line 1", "Bus1", "Bus2", bundle1, geometry1, 10)

print(f"Transmission Lines in circuit:", list(circuit1.transmission_line.keys()))

# Step 4: Verify Network Configuration
print("circuit Details:", circuit1)

# Step 5: Perform Edge Case Testing
try:
    circuit1.add_bus("Bus1", 230)
except ValueError as e:
    print("Error Caught:", e)

try:
    circuit1.add_transformer("T2", "Bus1", "Bus3", 100, 8, 10, 100)
except ValueError as e:
    print("Error Caught:", e)

try:
    circuit1.add_transmission_line("Line 2", "Bus1", "Bus3", bundle1, geometry1, 10)
except ValueError as e:
    print("‼️Error Caught:", e)

#if __name__ == '__main__':
