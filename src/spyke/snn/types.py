from spyke.snn import SpikingNeuronWrapper, ExtendableSpikingNeuron, Synapse
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


class STDPSpikingNeuron(SpikingNeuronWrapper):

    def __init__(self, A_p=1.0, A_n=1.0, tau_p=1.0, tau_n=1.0, min_p=0.0, max_p=1000, min_n=0.0, max_n=1000):
        super().__init__()
        self.last_fire_time_step = 0
        self.A_p = A_p
        self.tau_p = tau_p
        self.A_n = A_n
        self.tau_n = tau_n
        self.min_p = min_p
        self.max_p = max_p
        self.min_n = min_n
        self.max_n = max_n

    def on_fire(self, neuron: ExtendableSpikingNeuron, time_step: int):
        self.last_fire_time_step = time_step
        for synapse in neuron.connections:
            self._update_synapse(neuron, synapse, synapse.end_node)
        for back_synapse in neuron.back_refs:
            self._update_synapse(back_synapse.start_node, back_synapse.connection, neuron)

    def _update_synapse(self, pre: ExtendableSpikingNeuron, synapse: Synapse, post: ExtendableSpikingNeuron) -> None:
        pre_wrapper: STDPSpikingNeuron = pre.get_neuron_wrapper(STDPSpikingNeuron)
        post_wrapper: STDPSpikingNeuron = post.get_neuron_wrapper(STDPSpikingNeuron)
        if pre_wrapper is None or post_wrapper is None or (pre.is_fireing() and post.is_fireing()):
            return
        
        sign = 1 if synapse.weight >= 0.0 else -1
        dt = post_wrapper.last_fire_time_step - pre_wrapper.last_fire_time_step
        potentiation = dt >= 0.0
        dt_sign = -1 if potentiation else 1
        dA = self.A_p if potentiation else self.A_n
        dtau = self.tau_p if potentiation else self.tau_n
        dmin = self.min_p if potentiation else self.min_n
        dmax = self.max_p if potentiation else self.max_n

        diff = dA * math.exp(dt_sign * dt / dtau)
        synapse.weight += diff
        synapse.weight = sign * min(dmax, max(dmin, abs(synapse.weight)))
        