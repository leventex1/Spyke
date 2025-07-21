from spyke.snn import SpikingNeuron
import math


class LIFSpikingNeuron(SpikingNeuron):

    def __init__(self, 
                 reset_value = 0, 
                 membrane_value = 0, 
                 threshold_value = 1,
                 tau = 1.0
                ):
        super().__init__(reset_value, membrane_value, threshold_value)
        self.tau = tau

    def update(self, time_step: int) -> None:
        dt = time_step - self.last_updated_time_step
        self.membrane_value *= math.exp(-dt / self.tau)
        super().update(time_step)