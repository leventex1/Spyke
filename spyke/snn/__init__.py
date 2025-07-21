from typing import Callable
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

    def is_fireing(self) -> bool:
        return self.membrane_value >= self.threshold_value
    
    def fire_neuron(self):
        self.reset_neuron()
    
    def update(self, time_step) -> None:
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