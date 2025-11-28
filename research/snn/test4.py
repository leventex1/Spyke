import matplotlib.pyplot as plt
import math
import random
from research.snn import RecorderSN, InitialStimulus
from spyke.snn import Synapse, SpikingNeuron, SpikingNeuronWrapper, ExtendableSpikingNeuron
from spyke.networkengine import NetworkEngine
from research.tools.visualize import PrintNetwork


class IncrementalBrancher(SpikingNeuronWrapper):

    def __init__(self, branch_incrementation=1.0, tau=1.0):
        super().__init__()
        self.branching_value = 0.0
        self.branch_incrementation = branch_incrementation
        self.tau = tau
        self.last_fired_time_step = 0

    def on_fire(self, neuron, time_step):
        self.last_fired_time_step = time_step
        
        for synapse in neuron.connections:
            self._trigger_adjustments(synapse)

        for back_ref in neuron.back_refs:
            self._back_signal(back_ref.start_node, time_step)

        self.branching_value = -self.branch_incrementation

    def on_update(self, neuron, time_step):
        dt = time_step - neuron.last_updated_time_step
        self.branching_value *= math.exp(-dt / self.tau)

    def _trigger_adjustments(self, synapse: Synapse):
        synapse.weight -= 0.0 * self.branching_value

    def _back_signal(self, pre_neuron: ExtendableSpikingNeuron, time_step: int):
        pre_incremental_brancher: IncrementalBrancher = pre_neuron.get_neuron_wrapper(IncrementalBrancher)
        if time_step - pre_incremental_brancher.last_fired_time_step == 2:
            pre_incremental_brancher.branching_value += self.branch_incrementation

class TestNeuron(RecorderSN):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_sn_wrapper(IncrementalBrancher(tau=10))


class NetworkVisualizer(PrintNetwork):

    def neuron_id_format(self, neuron):
        return f"{neuron.id:2}: "

    def neuron_format(self, pre_neuron, synapse):
        return f"{synapse.weight:.2f}"


num_neurons = 20
connection_prob = 0.8
time_steps = 200
spike_times = [i for i in range(time_steps) if i % 2 == 1]
w_min = -0.26
w_max = 0.45
w_offset = 0

neurons: list[TestNeuron] = [TestNeuron() for _ in range(num_neurons)]
test_neuron = neurons[0]
test_neuron_branching_values: list[float] = []
for i in range(num_neurons):
    for j in range(num_neurons):
        if i == j:
            continue
        elif random.random() < connection_prob:
            w = w_offset + (w_min + random.random() * (w_max - w_min))
            neurons[i].add_connection(Synapse(w, neurons[j]))

network_visualizer = NetworkVisualizer(neurons, separator=" ")
print(network_visualizer)

engine = NetworkEngine()
engine.add_process(InitialStimulus(random.sample(neurons, k=4)))

brancher: IncrementalBrancher = test_neuron._wrappers[0]
for t in range(time_steps):
    test_neuron.update(t)
    engine.spin()
    test_neuron.update(t)
    test_neuron_branching_values.append(brancher.branching_value)

for n in neurons:
    n.print_spikes(spike_times, neuron_id_format=lambda id: f"{id:2}: ")

print()
avg_count = 0
len_count = 0
for i in range(len(spike_times)-1):
    count = 0
    if spike_times[i] in test_neuron.spikes:
        for synapse in test_neuron.connections:
            count += spike_times[i+1] in synapse.end_node.spikes
    if count:
        print(count, end=", ")
        len_count += 1
        avg_count += count

print()
if len_count:
    print(avg_count / len_count)
    """ plt.plot(test_neuron_branching_values)
    plt.grid(True)
    plt.show() """