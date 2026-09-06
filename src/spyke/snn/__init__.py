from spyke.neuron import Neuron
from spyke.graph import Connection


class SpikingNeuron(Neuron):
    """
    SpikingNeuron inherits the Neuron class.
    
    member variables:
    - self.threshold_value: float, indicates the spiking neurons membrane threshold value where the neuron fires.
    - self.last_updated_time_step: None | int, keeps track when the neuron is last updated. Helper variables for some attached dynamics.

    methods:
    - is_fireing(self) -> bool, returns True if the membrane_value is ">=" the threshold_value, otherwise returns False.
    """

    def __init__(self, 
        reset_value: float = 0.0,
        membrane_value: float = 0.0,
        threshold_value: float = 1.0
    ):
        super().__init__(reset_value, membrane_value)
        self.threshold_value: float = threshold_value
        self.last_updated_time_step: int = 0
        self.last_fire_time_step: int = None

    def is_fireing(self) -> bool:
        return self.membrane_value >= self.threshold_value
    
    def fire_neuron(self, time_step: int):
        self.last_fire_time_step = time_step
        self.reset_neuron()

        for synapse in self.connections:
            if isinstance(synapse, Synapse):
                synapse.on_spike(self, time_step)

        for back_ref in self.back_refs:
            if isinstance(back_ref.connection, Synapse):
                back_ref.connection.on_spike(back_ref.start_node, time_step)
    
    def update(self, time_step: int) -> None:
        self.last_updated_time_step = time_step
    

class Synapse(Connection):
    """
    Synapse is the child of Connection.
    Holds the synaptic weight and the time when the pre and post neurons last spiked.

    member variables:
    - self.weight: float
    """

    def __init__(self, weight: float, post_neuron: SpikingNeuron) -> None:
        super().__init__(post_neuron)
        self.weight = weight

    def on_spike(self, pre_neuron: SpikingNeuron, time_step: int) -> None:
        pass


class SpikingNeuronWrapper:
    """
    Base class for extending the spiking neuron dynamics.
    Example: LIFNeuron or AdaptiveThresholdNeuron or the combination of both.
    """

    def on_init(self, neuron: SpikingNeuron) -> None:
        pass

    def on_update(self, neuron: SpikingNeuron, time_step: int) -> None:
        pass

    def on_fire(self, neuron: SpikingNeuron, time_step: int) -> None:
        pass


class ExtendableSpikingNeuron(SpikingNeuron):
    """
    Handels the extentions of the spiking neuron.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._wrappers: list[SpikingNeuronWrapper] = []

    def add_sn_wrapper(self, sn_wrapper: SpikingNeuronWrapper) -> None:
        sn_wrapper.on_init(self)
        self._wrappers.append(sn_wrapper)

    def update(self, time_step: int) -> None:
        for wrapper in self._wrappers:
            wrapper.on_update(self, time_step)
        super().update(time_step)

    def fire_neuron(self, time_step: int) -> None:
        for wrapper in self._wrappers:
            wrapper.on_fire(self, time_step)
        return super().fire_neuron(time_step)
    
    def get_neuron_wrapper(self, wrapper_type: SpikingNeuronWrapper) -> SpikingNeuronWrapper | None:
        for wrapper in self._wrappers:
            if isinstance(wrapper, wrapper_type):
                return wrapper
        return None
