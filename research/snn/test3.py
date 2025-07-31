import random
from research.snn import RecorderSN, InitialStimulus
from spyke.snn import Synapse
from spyke.networkengine import NetworkEngine
from research.tools.visualize import PrintNetwork
from spyke.snn.types import LIFSpikingNeuron, AdaptiveThSpikingNeuron, STDPSpikingNeuron

num_neurons = 10
time_steps = 100
connection_prob = 0.3
excitation_prob = 0.8

neurons: list[RecorderSN] = []
for i in range(num_neurons):
    neurons.append(RecorderSN())

for i, src in enumerate(neurons):
    for j, tgt in enumerate(neurons):
        if random.random() < connection_prob:
            weight = random.random() * 1.5 if random.random() < excitation_prob else random.random() * -0.2
            src.add_connection(Synapse(weight, tgt))

engine = NetworkEngine()
stimulated = random.sample(neurons, k=3)
engine.add_process(InitialStimulus(stimulated))

for _ in range(time_steps):
    engine.spin()

print_network = PrintNetwork(neurons)
print(print_network)

for n in neurons:
    n.print_spikes(time_steps)

spikes = []
for t in range(time_steps):
    count = 0
    for neuron in neurons:
        count += t in neuron.spikes
    if count:
        spikes.append(count)

average_br = 0
for i in range(len(spikes)-1):
    branching_ratio = spikes[i+1] / spikes[i]
    average_br += branching_ratio
    print(f"{branching_ratio:.1f}", end=" ")
average_br /= len(spikes)
print(f"\naverage br: {average_br:.4f}")

for neuron in neurons:
    neuron.add_sn_wrapper(LIFSpikingNeuron(12))
    neuron.add_sn_wrapper(AdaptiveThSpikingNeuron(0.2, 10))
    #neuron.add_sn_wrapper(STDPSpikingNeuron(A_p=0.02, tau_p=5, A_n=-0.02, tau_n=5, max_p=1.5, max_n=0.5))
    neuron.spikes.clear()
    neuron.reset_neuron()

engine.reset()
engine.add_process(InitialStimulus(stimulated))
for _ in range(time_steps):
    engine.spin()

for n in neurons:
    n.print_spikes(time_steps)

spikes = []
for t in range(time_steps):
    count = 0
    for neuron in neurons:
        count += t in neuron.spikes
    if count:
        spikes.append(count)

average_br = 0
for i in range(len(spikes)-1):
    branching_ratio = spikes[i+1] / spikes[i]
    average_br += branching_ratio
    print(f"{branching_ratio:.1f}", end=" ")
average_br /= len(spikes)
print(f"\naverage br: {average_br:.4f}")
