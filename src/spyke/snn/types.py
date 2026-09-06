from spyke.snn import SpikingNeuronWrapper, ExtendableSpikingNeuron, Synapse, SpikingNeuron
import math


class LIFSpikingNeuron(SpikingNeuronWrapper):

    def __init__(self, tau=1.0):
        super().__init__()
        self.tau = tau

    def on_update(self, neuron, time_step: int) -> None:
        dt = time_step - neuron.last_updated_time_step
        neuron.membrane_value *= math.exp(-dt / self.tau)


class AdaptiveThSpikingNeuron(SpikingNeuronWrapper):
    
    def __init__(self, th_increment=0.1, tau=1.0):
        super().__init__()
        self.base_threshold: float = 1.0
        self.th_increment = th_increment
        self.tau = tau

    def on_init(self, neuron):
        self.base_threshold = neuron.threshold_value

    def on_update(self, neuron, time_step):
        dt = time_step - neuron.last_updated_time_step
        diff = neuron.threshold_value - self.base_threshold
        diff *= math.exp(-dt / self.tau)
        neuron.threshold_value = self.base_threshold + diff

    def on_fire(self, neuron, _):
        neuron.threshold_value += self.th_increment


class PlasticSynapse(Synapse):

    def __init__(self, weight, post_neuron, ltp: tuple[float, float], ltd: tuple[float, float], min: float, max: float, mu: float = 0):
        self.ltp = ltp
        self.ltd = ltd
        self.min = min
        self.max = max
        self.mu = mu
        super().__init__(weight, post_neuron)

    def on_spike(self, pre_neuron: SpikingNeuron, time_step) -> None:
        post_neuron: SpikingNeuron = self.end_node

        if pre_neuron.last_fire_time_step is None or post_neuron.last_fire_time_step is None:
            return

        if pre_neuron.is_fireing() and post_neuron.is_fireing():
            return

        dt = post_neuron.last_fire_time_step - pre_neuron.last_fire_time_step
        potentiation = dt > 0.0
        amp, tau = self.ltp if potentiation else self.ltd

        delta = amp * math.exp(-1.0 * abs(dt) / tau)
        dist = self.max - self.weight if potentiation else self.weight - self.min
        diff = delta * dist**self.mu

        self.weight += diff
