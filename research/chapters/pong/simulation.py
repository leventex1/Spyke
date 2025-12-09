from research.chapters.pong.game import GameInterface, Vector
from spyke.networkengine import NetworkEngine
from spyke.snn import SpikingNeuron, ExtendableSpikingNeuron, Synapse, SpikingNeuronWrapper
from spyke.snn.networkengine import FireQueueProcess
from spyke.snn.types import LIFSpikingNeuron
import random
import math
from typing import Callable


min_w = -0.5
max_w = 0.5

class OutputSpikingNeuron(SpikingNeuronWrapper):
    
    def __init__(self, on_fire_cb: Callable):
        super().__init__()
        self.on_fire_cb = on_fire_cb

    def on_fire(self, neuron, time_step):
        self.on_fire_cb()


class Network:
 
    def __init__(self):
        self.outputs = [0, 0]
        self.neurons: list[SpikingNeuron] = []
        for i in range(100):
            neuron = ExtendableSpikingNeuron()
            neuron.add_sn_wrapper(LIFSpikingNeuron(2.0))
            if i >= 50 and i < 75:
                neuron.add_sn_wrapper(OutputSpikingNeuron(lambda: self.increment_output(0)))
            elif i >= 75:
                neuron.add_sn_wrapper(OutputSpikingNeuron(lambda: self.increment_output(1)))
            self.neurons.append(neuron)
        
        for i in range(len(self.neurons)):
            for j in range(len(self.neurons)):
                if i == j:
                    continue
                self.neurons[i].add_connection(Synapse(min_w + random.random() * (max_w - min_w), self.neurons[j]))

        self.engine = NetworkEngine()

    def increment_output(self, index: int):
        self.outputs[index] += 1

    def update(self, inputs: list[int]):
        for i in range(len(inputs)):
            if inputs[i] == 1:
                self.neurons[i].membrane_value = 1000
                self.engine.add_process(FireQueueProcess(self.neurons[i]))
        self.engine.spin()
    
    def check_output(self) -> tuple[bool, bool]:
        if self.outputs[0] < 10 and self.outputs[1] < 10:
            return (False, False)
         
        move_left = False 
        move_right = False
        if self.outputs[0] >= 10:
            move_left = True
        if self.outputs[1] >= 10:
            move_right = True
        
        self.outputs = [0, 0]
        return (move_left, move_right)


if __name__ == "__main__":
    gi = GameInterface(1211, 1.0 / 10.0, Vector(1.0 / math.sqrt(2), 1.0 / math.sqrt(2)))
    network = Network()
    for i in range(100):
        inputs = gi.get_inputs(10, 0.1, 0.6)
        network.update(inputs)
        move_left, move_right = network.check_output()
        is_game_over, is_ball_hit = gi.update(-1 * int(move_left) + 1 * int(move_right))
        
        print(f"{i+1:02}", inputs, f"{gi.game.paddle_pos.x:.2f}", network.outputs, move_left, move_right)
        if is_game_over:
            print("Game over")
            break
        elif is_ball_hit:
            print("Ball hit")
