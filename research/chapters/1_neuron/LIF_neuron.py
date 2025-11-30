from research.snn import RecorderSN
from spyke.snn import SpikingNeuron, Synapse
from spyke.snn.types import LIFSpikingNeuron
from spyke.networkengine import NetworkEngine
from spyke.snn.networkengine import FireQueueProcess
import matplotlib.pyplot as plt
import numpy as np

engine = NetworkEngine()

input_neuron = SpikingNeuron(0, 1, 1)
neuron_LIF = RecorderSN(0, 0, 0.15)
neuron_LIF.add_sn_wrapper(LIFSpikingNeuron(8))
input_neuron.add_connection(Synapse(0.07, neuron_LIF))

time_steps = 100
membrane_values = np.zeros((time_steps, ))
for i in range(time_steps):
    neuron_LIF.update(engine.time_step)
    membrane_values[i] = neuron_LIF.membrane_value
    if i >= time_steps // 2 - 3 * 4 and i <= time_steps // 2 - 1 and i % 2 == 0:
        input_neuron.membrane_value = 1.5
        engine.add_process(FireQueueProcess(input_neuron))
    engine.spin()

x = []
y = []
eps = 1e-9
for i in range(len(membrane_values)):
    if i not in neuron_LIF.spikes:
        x.append(i)
        y.append(membrane_values[i])
    else:
        x.append(i)
        y.append(1)

fig, ax = plt.subplots()
ax.set_title("Integrate and fire neuron")
ax.plot(x, y)
ax.set_xlabel("Time steps")
ax.set_ylabel("Membrane value")
ax.axhline(neuron_LIF.threshold_value, color="gray", linestyle="--", linewidth=1)
ax.text(time_steps // 2 - 30 + 2 * 0.5, neuron_LIF.threshold_value, "Threshold", color="gray", verticalalignment="bottom", horizontalalignment="left")
ax.set_xbound(time_steps // 2 - 30, time_steps // 2 + 30)
plt.show()
