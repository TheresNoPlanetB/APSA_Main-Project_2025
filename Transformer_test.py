from transformer import Transformer
from bus import Bus

bus1 = Bus("Bus 1", 230)
bus2 = Bus("Bus 2", 230)
transformer1 = Transformer("T1", bus1, bus2, 125, 8.5, 10, 100)
print(f"Name:{transformer1.name}, Bus1 name:{transformer1.bus1.name}, Bus2 name:{transformer1.bus2.name}, power rating:{transformer1.power_rating}, impedance_percent:{transformer1.impedance_percent}, x_over_r_ratio:{transformer1.x_over_r_ratio}")
print(f"impedance{transformer1.zt}, admittance{transformer1.yt}")
print(f" matrix validation:{transformer1.yprim}")

