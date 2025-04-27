import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
from sym_components import abc_to_seq, seq_to_abc

# Helper function to plot one bus
def plot_one_bus(ax, currents, voltages, bus_id):
    Ia, Ib, Ic = currents
    Va, Vb, Vc = voltages

    # Symmetrical components for currents
    v0_c, v1_c, v2_c = abc_to_seq(Ia, Ib, Ic)
    ia_0, ib_0, ic_0 = seq_to_abc(v0_c, 0, 0)
    ia_1, ib_1, ic_1 = seq_to_abc(0, v1_c, 0)
    ia_2, ib_2, ic_2 = seq_to_abc(0, 0, v2_c)

    # Symmetrical components for voltages
    v0_v, v1_v, v2_v = abc_to_seq(Va, Vb, Vc)
    va_0, vb_0, vc_0 = seq_to_abc(v0_v, 0, 0)
    va_1, vb_1, vc_1 = seq_to_abc(0, v1_v, 0)
    va_2, vb_2, vc_2 = seq_to_abc(0, 0, v2_v)

    current_colors = {'positive': 'green', 'negative': 'blue', 'zero': 'red'}
    voltage_colors = {'positive': 'orange', 'negative': 'purple', 'zero': 'brown'}

    vectors_currents = {
        'positive': [ia_1, ib_1, ic_1],
        'negative': [ia_2, ib_2, ic_2],
        'zero': [ia_0, ib_0, ic_0]
    }
    vectors_voltages = {
        'positive': [va_1, vb_1, vc_1],
        'negative': [va_2, vb_2, vc_2],
        'zero': [va_0, vb_0, vc_0]
    }

    for seq_type, vec_list in vectors_currents.items():
        for vec in vec_list:
            ax.arrow(0, 0, vec.real, vec.imag,
                     color=current_colors[seq_type],
                     head_width=0.02, head_length=0.04,
                     length_includes_head=True)

    for seq_type, vec_list in vectors_voltages.items():
        for vec in vec_list:
            ax.plot([0, vec.real], [0, vec.imag], linestyle='--', color=voltage_colors[seq_type])
            ax.plot(vec.real, vec.imag, marker='o', color=voltage_colors[seq_type])

    ax.set_title(f'Bus {bus_id}', fontsize=10)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.grid(True)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([-2, -1, 0, 1, 2])

# Class to manage interactive navigation
class PlotIterator:
    def __init__(self, all_fault_data):
        self.all_fault_data = all_fault_data
        self.current = 0
        self.fig, self.axs = plt.subplots(2, 4, figsize=(22, 12))
        self.axs = self.axs.flatten()

        # Buttons further left
        axprev = self.fig.add_axes([0.01, 0.01, 0.08, 0.04])
        axnext = self.fig.add_axes([0.10, 0.01, 0.08, 0.04])
        self.bprev = Button(axprev, 'Previous')
        self.bnext = Button(axnext, 'Next')

        self.bnext.on_clicked(self.next_page)
        self.bprev.on_clicked(self.previous_page)

    def plot_page(self, event=None):
        fault, fault_currents, fault_voltages = self.all_fault_data[self.current]

        for ax in self.axs:
            ax.clear()

        for idx, bus_id in enumerate(range(1, 8)):
            plot_one_bus(self.axs[idx], fault_currents[bus_id], fault_voltages[bus_id], bus_id)

        # Summary table on the last subplot
        self.axs[-1].axis('off')
        table_data = []
        for bus_id in range(1, 8):
            Ia, Ib, Ic = fault_currents[bus_id]
            Va, Vb, Vc = fault_voltages[bus_id]
            # Fault Current Sequences
            I0, I1, I2 = abc_to_seq(Ia, Ib, Ic)
            # Fault Voltage Sequences
            V0, V1, V2 = abc_to_seq(Va, Vb, Vc)
            table_data.append([
                f"Bus {bus_id}",
                f"{abs(I1):.2f}∠{np.angle(I1, deg=True):.1f}°",
                f"{abs(I2):.2f}∠{np.angle(I2, deg=True):.1f}°",
                f"{abs(I0):.2f}∠{np.angle(I0, deg=True):.1f}°",
                f"{abs(V1):.2f}∠{np.angle(V1, deg=True):.1f}°",
                f"{abs(V2):.2f}∠{np.angle(V2, deg=True):.1f}°",
                f"{abs(V0):.2f}∠{np.angle(V0, deg=True):.1f}°"
            ])

        col_labels = ["Bus", "|I₁|∠θ₁", "|I₂|∠θ₂", "|I₀|∠θ₀", "|V₁|∠θ₁", "|V₂|∠θ₂", "|V₀|∠θ₀"]
        self.axs[-1].table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
        self.axs[-1].set_title("Fault Summary", fontsize=10)

        # Add shared legend
        custom_lines = [
            Line2D([0], [0], color='green', lw=2, label='Current Positive Sequence'),
            Line2D([0], [0], color='blue', lw=2, label='Current Negative Sequence'),
            Line2D([0], [0], color='red', lw=2, label='Current Zero Sequence'),
            Line2D([0], [0], color='orange', lw=2, linestyle='--', marker='o', label='Voltage Positive Sequence'),
            Line2D([0], [0], color='purple', lw=2, linestyle='--', marker='o', label='Voltage Negative Sequence'),
            Line2D([0], [0], color='brown', lw=2, linestyle='--', marker='o', label='Voltage Zero Sequence')
        ]
        self.fig.legend(handles=custom_lines, loc='lower center', ncol=3, fontsize=10)

        self.fig.suptitle(f"{fault} Fault - Bus Sequence Vectors", fontsize=18)
        plt.tight_layout(rect=[0, 0.08, 1, 0.92])
        plt.draw()

    def next_page(self, event=None):
        if self.current < len(self.all_fault_data) - 1:
            self.current += 1
            self.plot_page()
        else:
            print("Reached end of faults.")

    def previous_page(self, event=None):
        if self.current > 0:
            self.current -= 1
            self.plot_page()
        else:
            print("Already at first fault.")

# Main function
def generate_fault_plots(circuit):
    """
    Interactive multi-page plotting with Next and Previous buttons.
    """
    fault_types = ["Symmetrical", "SLG", "LL", "DLG"]
    all_fault_data = []

    # Prepare all data
    for idx, fault in enumerate(fault_types):
        if idx >= len(circuit.fault_currents) or not circuit.fault_currents[idx]:
            print(f"{fault} fault not found. Simulating random values for plotting...")
            fault_currents = {}
            fault_voltages = {}
            for bus_id in range(1, 8):
                Ia = np.random.uniform(0, 12) * np.exp(1j * np.random.uniform(-180, 180))
                Ib = np.random.uniform(0, 12) * np.exp(1j * np.random.uniform(-180, 180))
                Ic = np.random.uniform(0, 12) * np.exp(1j * np.random.uniform(-180, 180))
                Va = np.random.uniform(0.4, 1.05) * np.exp(1j * np.random.uniform(-180, 180))
                Vb = np.random.uniform(0.4, 1.05) * np.exp(1j * np.random.uniform(-180, 180))
                Vc = np.random.uniform(0.4, 1.05) * np.exp(1j * np.random.uniform(-180, 180))
                fault_currents[bus_id] = (Ia, Ib, Ic)
                fault_voltages[bus_id] = (Va, Vb, Vc)
        else:
            fault_currents = circuit.fault_currents[idx]
            fault_voltages = circuit.fault_bus_vs[idx]

        all_fault_data.append((fault, fault_currents, fault_voltages))

    # Start plotting
    plotter = PlotIterator(all_fault_data)
    plotter.plot_page()
    plt.show()
