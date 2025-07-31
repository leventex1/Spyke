from spyke.neuron import Neuron
from spyke.snn import Synapse


class PrintNetwork:

    def __init__(self, neurons: list[Neuron], separator: str="    "):
        self.neurons = neurons
        self.separator = separator

    def format(self) -> None:
        pass

    def neuron_id_format(self, neuron: Neuron) -> str:
        return f"{neuron.id}: "

    def neuron_format(self, pre_neuron: Neuron, synapse: Synapse) -> str:
        s = "+" if synapse.weight > 0 else "-"
        return f"{pre_neuron.id} ({s}{abs(synapse.weight):.2f})-> {synapse.end_node.id}"

    def __str__(self):
        self.format()
        res = ""
        for neuron in self.neurons:
            res += self.neuron_id_format(neuron)
            for synapse in neuron.connections:
                res += self.neuron_format(neuron, synapse) + self.separator
            res += "\n"
        return res