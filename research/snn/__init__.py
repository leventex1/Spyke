from spyke.snn import SpikingNeuron, ExtendableSpikingNeuron
from spyke.snn.networkengine import FireQueueProcess, QueueProcess
from typing import Callable


class RecorderSN(ExtendableSpikingNeuron):

    def __init__(self, reset_value = 0, membrane_value = 0, threshold_value = 1, **kwargs):
        super().__init__(reset_value, membrane_value, threshold_value, **kwargs)
        self.spikes = set()

    def fire_neuron(self, time_step: int):
        self.spikes.add(self.last_updated_time_step)
        return super().fire_neuron(time_step)
    
    def print_spikes(self, time_steps: int | list[int], neuron_id_format: Callable[[int], str] | None=None):
        id_format = neuron_id_format(self.id) if neuron_id_format is not None else f"{self.id}"
        print(id_format, end="")
        if isinstance(time_steps, int):
            for t in range(time_steps):
                if t in self.spikes:
                    print("|", end="")
                else:
                    print(".", end="")
        else:
            for t in time_steps:
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
            neuron.membrane_value = neuron.threshold_value * 1000 # safe 1000 times
        return [FireQueueProcess(n) for n in self.targets]

    def is_primary_process(self) -> bool:
        return True