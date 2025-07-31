import math
import random
from research.snn import RecorderSN, InitialStimulus
from spyke.snn import Synapse, SpikingNeuron, SpikingNeuronWrapper
from spyke.networkengine import NetworkEngine
from research.tools.visualize import PrintNetwork


class IncrementalBranching(SpikingNeuronWrapper):

    def __init__(self, branch_incrementation=1.0, tau=1.0):
        super().__init__()
        self.branching_value = 0
        self.branch_incrementation = branch_incrementation
        self.tau = tau

    def on_fire(self, neuron):
        self._trigger_adjustments(neuron)

    def on_update(self, neuron, time_step):
        dt = time_step - neuron.last_updated_time_step
        self.branching_value *= math.exp(-dt / self.tau)

    def _trigger_adjustments(self, neuron):
        # do weight adjustments
        self.branching_value = self.branch_incrementation


class TestNeuron(RecorderSN):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NetworkVisualizer(PrintNetwork):

    def neuron_id_format(self, neuron):
        return f"{neuron.id:2}: "

    def neuron_format(self, pre_neuron, synapse):
        return f"{synapse.weight:.2f}"


num_neurons = 20
time_steps = 200
spike_times = [i for i in range(time_steps) if i % 2 == 1]
w_min = -0.28
w_max = 0.4
w_offset = 0

neurons: list[TestNeuron] = [TestNeuron() for _ in range(num_neurons)]
for i in range(num_neurons):
    for j in range(num_neurons):
        if i == j:
            continue
        else:
            w = w_offset + (w_min + random.random() * (w_max - w_min))
            neurons[i].add_connection(Synapse(w, neurons[j]))

network_visualizer = NetworkVisualizer(neurons, separator=" ")
print(network_visualizer)

engine = NetworkEngine()
engine.add_process(InitialStimulus(random.sample(neurons, k=5)))

for t in range(time_steps):
    engine.spin()

for n in neurons:
    n.print_spikes(spike_times, neuron_id_format=lambda id: f"{id:2}: ")

print()
neuron = neurons[0]
avg_count = 0
len_count = 0
for i in range(len(spike_times)-1):
    count = 0
    if spike_times[i] in neuron.spikes:
        for synapse in neuron.connections:
            count += spike_times[i+1] in synapse.end_node.spikes
    if count:
        print(count, end=", ")
        len_count += 1
        avg_count += count

print()
if len_count:
    print(avg_count / len_count)