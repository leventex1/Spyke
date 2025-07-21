from spyke.graph import Node


class Neuron(Node):
    """
    Neuron class is the base implementation of a digital artificial neuron.
    This class can be extended to behave differently with all kind of neural networks, like SNN or simple ANN.

    static variables:
    - ID: int, keep track of the newly created neuron's id.

    member variables:
    - self.resert_value: float, the value where the membrane_value will be reseted after calling self.reset_neuron().
    - self.membrane_value: float, holds the neuron's membrane "potential" value.
    - self.id: int, a unique id that identifies the neuron, for debug purposes.

    methods:
    - change_membrane_value(self, change: float) -> None, changes the membrane_value with change.
    - reset_neuron(self) -> None, set the self.membrane_value to the self.resert_value.
    """
    ID: int = 0

    def __init__(self,
            reset_value: float, 
            membrane_value: float
        ) -> None:
        super().__init__()
        self.reset_value: float = reset_value
        self.membrane_value: float = membrane_value
        self.id: int = Neuron.ID
        Neuron.ID += 1

    def change_membrane_value(self, change: float) -> None:
        self.membrane_value += change
    
    def reset_neuron(self) -> None:
        self.membrane_value = self.reset_value