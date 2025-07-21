import random
from research.snn import RecorderSN, InitialStimulus
from spyke.snn import Synapse
from spyke.snn.types import LIFSpikingNeuron
from spyke.networkengine import NetworkEngine
from research.tools.visualize import PrintNetwork

RecorderSN.__bases__ = (LIFSpikingNeuron, )

# --- Config ---
#random.seed(42)
num_neurons = 20
time_steps = 200
connection_prob = 0.2
excitation_prob = 0.5

# --- Create neurons ---
neurons: list[RecorderSN] = []
for i in range(num_neurons):
    #threshold = random.uniform(0.7, 1.3)
    n = RecorderSN(threshold_value=1.0, tau=18)
    n.id = f"N{i:02}"
    neurons.append(n)

# Assign excitatory or inhibitory roles

# --- Connect neurons randomly ---
for i, src in enumerate(neurons):
    for j, tgt in enumerate(neurons):
        if random.random() < connection_prob:
            weight = random.random() * 1.5 if random.random() < excitation_prob else random.random() * -0.5
            src.add_connection(Synapse(weight, tgt))

# --- Create engine and stimulus ---
engine = NetworkEngine()
stimulated = random.sample(neurons, k=5)
engine.add_process(InitialStimulus(stimulated))

# --- Run simulation ---
for _ in range(time_steps):
    engine.spin()

print_network = PrintNetwork(neurons)
print(print_network)

# --- Print results ---
print("Spike Trains:")
for n in neurons:
    n.print_spikes(time_steps)