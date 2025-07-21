from spyke.snn import SpikingNeuron
from spyke.snn.networkengine import FireQueueProcess, QueueProcess


class RecorderSN(SpikingNeuron):

    def __init__(self, reset_value = 0, membrane_value = 0, threshold_value = 1, **kwargs):
        super().__init__(reset_value, membrane_value, threshold_value, **kwargs)
        self.spikes = set()

    def fire_neuron(self):
        self.spikes.add(self.last_updated_time_step)
        return super().fire_neuron()
    
    def print_spikes(self, time_steps: int):
        print(f"{self.id}: ", end="")
        for t in range(time_steps):
            if t in self.spikes:
                print("|", end="")
            else:
                print(".", end="")
        print()


class InitialStimulus(QueueProcess):
    def __init__(self, targets: list[SpikingNeuron]):
        self.targets = targets

    def process(self, _: int) -> list[QueueProcess]:
        for neuron in self.targets:
            neuron.membrane_value = neuron.threshold_value * 2 # safe 2 times
        return [FireQueueProcess(n) for n in self.targets]

    def is_primary_process(self) -> bool:
        return True