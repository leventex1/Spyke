from spyke.networkengine import QueueProcess
from spyke.snn import SpikingNeuron, Synapse


class SendSpikeQueueProcess(QueueProcess):

    def __init__(self, synapse: Synapse):
        self.synapse = synapse

    def process(self, _: int) -> list[QueueProcess]:
        post_neuron: SpikingNeuron = self.synapse.end_node
        post_neuron.change_membrane_value(self.synapse.weight)
        return [FireQueueProcess(post_neuron)]
    
    def is_primary_process(self) -> bool:
        return False


class FireQueueProcess(QueueProcess):

    def __init__(self, neuron: SpikingNeuron):
        self.neuron = neuron        

    def process(self, time_step: int) -> list[QueueProcess]:
        self.neuron.update(time_step)

        if not self.neuron.is_fireing():
            return []
        
        self.neuron.fire_neuron(time_step)
        return [SendSpikeQueueProcess(synapse) for synapse in self.neuron.connections]
        
    def is_primary_process(self) -> bool:
        return True