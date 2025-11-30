from research.snn import RecorderSN
from spyke.snn import SpikingNeuron, Synapse
from spyke.networkengine import NetworkEngine
from spyke.snn.networkengine import FireQueueProcess
import matplotlib.pyplot as plt
import numpy as np


engine = NetworkEngine()

input_neuron = SpikingNeuron(0, 1, 1)
neuron_IF = RecorderSN(0, 0, 0.2)
input_neuron.add_connection(Synapse(0.07, neuron_IF))


time_steps = 10
membrane_values = np.zeros((time_steps, ))
for i in range(time_steps):
    membrane_values[i] = neuron_IF.membrane_value
    if i >= time_steps // 2 - 3 and i <= time_steps // 2 - 1:
        input_neuron.membrane_value = 1
        engine.add_process(FireQueueProcess(input_neuron))
    engine.spin()

x = []
y = []
eps = 1e-9
for i in range(len(membrane_values)):
    if i not in neuron_IF.spikes:
        x.append(i)
        y.append(membrane_values[i])
    else:
        prev_val = membrane_values[i-1] if i > 0 else 0
        next_val = membrane_values[i]
        x.extend([i-eps, i, i+eps])
        y.extend([prev_val, 1, next_val])

fig, ax = plt.subplots()
ax.set_title("Integrate and fire neuron")
ax.step(x, y)
ax.set_xlabel("Time steps")
ax.set_ylabel("Membrane value")
ax.axhline(neuron_IF.threshold_value, color="gray", linestyle="--", linewidth=1)
ax.text(0.02, neuron_IF.threshold_value, "Threshold", color="gray", verticalalignment="bottom", horizontalalignment="left")
plt.show()
