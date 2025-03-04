import numpy as np

def compute_power_injection(bus, ybus, voltages):

    bus_index = bus['index']
    bus_type = bus['bus_type']

    V_i = voltages[bus_index] # Gets voltage from bus i
    S_i = V_i * np.sum(ybus[bus_index, :] * np.conj(voltages)) # Complex power equation
    P_i = np.real(S_i) # Real Power
    Q_i = np.imag(S_i) # Reactive Power


    # Different bus types
    if bus_type == "Slack":
        return P_i, Q_i # Swing bus (slack bus) calculates P & Q
    elif bus_type == "PQ":
        return P_i, Q_i # Load (PQ) bus calculates P & Q
    elif bus_type == "PV":
        return P_i, None # Voltage controlled (PV) bus calculates only P
    else:
        raise ValueError("Unknown bus type: {bus_type}") # Incorrect bus type

if __name__ == '__main__':

    # System admittance matrix (Ybus)
    Ybus = np.array([[1+2j, 3+4j, 5+6j],
                     [7-8j,  9-1j, -2-3j],
                     [-4+5j, 6-7j,  -9+9j]])

    # Complex voltage
    Voltages = np.array([1.0 + 0j, 0.95 - 0.05j, 0.90 + 0.1j])

    # Bus input
    buses = [{'index': 0, 'bus_type': 'Slack'},
             {'index': 1, 'bus_type': 'PQ'},
             {'index': 2, 'bus_type': 'PV'}]

    # Compute power injections for each bus
    for bus in buses:
        P, Q = compute_power_injection(bus, Ybus, Voltages)
        Q_display = f"{Q:.4f}" if Q is not None else "n/a"
        print(f"Bus {bus['index']} ({bus['bus_type']}) - P: {P:.4f} p.u., Q: {Q_display} p.u.")