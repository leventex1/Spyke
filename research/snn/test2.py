import random
from research.snn import RecorderSN, InitialStimulus
from spyke.snn import Synapse
from spyke.snn.types import LIFSpikingNeuron, AdaptiveThSpikingNeuron, STDPSpikingNeuron
from spyke.networkengine import NetworkEngine
from research.tools.visualize import PrintNetwork


class Test2NeuronClass(RecorderSN):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_sn_wrapper(LIFSpikingNeuron(12))
        self.add_sn_wrapper(AdaptiveThSpikingNeuron(0.2, 10))
        self.add_sn_wrapper(STDPSpikingNeuron(A_p=0.02, tau_p=5, A_n=-0.04, tau_n=5, max_p=1.5, max_n=0.5))


# --- Config ---
#random.seed(42)
num_neurons = 20
time_steps = 220
connection_prob = 0.3
excitation_prob = 0.8

# --- Create neurons ---
neurons: list[Test2NeuronClass] = []
for i in range(num_neurons):
    #threshold = random.uniform(0.7, 1.3)
    n = Test2NeuronClass()
    n.id = f"N{i:02}"
    neurons.append(n)

# Assign excitatory or inhibitory roles

# --- Connect neurons randomly ---
for i, src in enumerate(neurons):
    for j, tgt in enumerate(neurons):
        if random.random() < connection_prob:
            weight = random.random() * 1.5 if random.random() < excitation_prob else random.random() * -0.2
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