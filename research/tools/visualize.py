from spyke.neuron import Neuron
from spyke.snn import Synapse


class PrintNetwork:

    def __init__(self, neurons: list[Neuron]):
        self.neurons = neurons

    def format(self) -> None:
        pass

    def neuron_format(self, pre_neuron: Neuron, synapse: Synapse) -> str:
        s = "+" if synapse.weight > 0 else "-"
        return f"{pre_neuron.id} ({s}{abs(synapse.weight):.2f})-> {synapse.end_node.id}"

    def __str__(self):
        self.format()
        res = ""
        for neuron in self.neurons:
            res += f"{neuron.id}: "
            for synapse in neuron.connections:
                res += self.neuron_format(neuron, synapse) + "    "
            res += "\n"
        return res