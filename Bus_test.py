from Bus import Bus

bus1 = Bus("Bus 1", 20)
bus2 = Bus("Bus 2", 230)
print(bus1.name, str(bus1.base_kv) + "kv", "index:" + str(bus1.index))
print(bus2.name, str(bus2.base_kv) + "kv", "index:" + str(bus2.index))
print(f"Total Number of Buses: {Bus.bus_count}")



