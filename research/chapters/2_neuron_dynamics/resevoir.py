from spyke.networkengine import NetworkEngine
from spyke.snn.networkengine import FireQueueProcess
from research.snn import RecorderSN
from spyke.snn import Synapse
from spyke.snn.types import LIFSpikingNeuron
import random
import numpy as np
from matplotlib import pyplot as plt

seed = 1211
simulation_time_steps = 5000
number_of_neurons = 50
connection_probability = 0.2
exctitation_probability = 0.5
relative_excitatory_strength = 1 / 15
relative_inhibitory_strength = 5 / 15
synaptic_strength = 0.3

v_reset = 0 #-65
v_threshold = 1 #-50
leaky_tau = 20

poison_input_firing_rate_range = (100, 1000)
poison_input_weight_range = (0.1, 2) #(0.01, 0.1)
show_neurons = 10
show_time_steps = 300

random.seed(seed)

poison_input_firing_rates: list[float] = []
poison_input_firing_weights: list[float] = []
for i in range(number_of_neurons):
    rate = poison_input_firing_rate_range[0] + (poison_input_firing_rate_range[1] - poison_input_firing_rate_range[0]) * random.random()
    weight = poison_input_weight_range[0] + (poison_input_weight_range[1] - poison_input_weight_range[0]) * random.random()
    poison_input_firing_rates.append(int(rate))
    poison_input_firing_weights.append(weight)

neurons: list[RecorderSN] = []
for i in range(number_of_neurons):
    neuron = RecorderSN(v_reset, v_reset, v_threshold)
    neuron.add_sn_wrapper(LIFSpikingNeuron(leaky_tau))
    neurons.append(neuron)

for neuron_a in neurons:
    for neuron_b in neurons:
        if neuron_a is neuron_b:
            continue
        elif random.random() >= connection_probability:
            continue

        weight = relative_excitatory_strength if random.random() < exctitation_probability else -relative_inhibitory_strength
        neuron_a.add_connection(Synapse(weight * synaptic_strength, neuron_b))


data_potentials: list[list[float]] = [[] for _ in range(number_of_neurons)]

engine = NetworkEngine()

for time_step in range(simulation_time_steps):
    for i, neuron in enumerate(neurons):
        if (time_step + 1) % poison_input_firing_rates[i] == 0:
            neuron.change_membrane_value(poison_input_firing_weights[i])
        engine.add_process(FireQueueProcess(neuron))
        data_potentials[i].append(neuron.membrane_value)
    
    engine.spin()

num_spikes = 0
for neuron in neurons:
    num_spikes += len(neuron.spikes)
print(f"number of spykes: {num_spikes}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), sharex=True, sharey=True, constrained_layout=True)

ax1.eventplot([list(neurons[n].spikes) for n in range(show_neurons)], linelengths=0.75)
for n in range(show_neurons):
    trace = np.array(data_potentials[n][:show_time_steps])
    trace = trace - trace.mean()
    trace = trace / (np.max(np.abs(trace)) + 1e-9) * 0.4
    ax2.plot(range(show_time_steps), trace + n)

ax1.set_xlim(0, show_time_steps)
ax1.set_yticks(range(show_neurons), [f"neuron {n+1}" for n in range(show_neurons)])
ax2.set_yticks(range(show_neurons))
plt.show()
