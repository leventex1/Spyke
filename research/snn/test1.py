from research.snn import RecorderSN, InitialStimulus
from spyke.snn.networkengine import Synapse, FireQueueProcess
from spyke.networkengine import NetworkEngine


time_steps = 100
n1 = RecorderSN()
n2 = RecorderSN()
n3 = RecorderSN()

n1.add_connection(Synapse(1.0, n2))
n2.add_connection(Synapse(1.0, n3))
n3.add_connection(Synapse(1.0, n1))

engine = NetworkEngine()

engine.add_process(InitialStimulus([n1]))
for t in range(time_steps):
    engine.spin()

n1.print_spikes(time_steps)
n2.print_spikes(time_steps)
n3.print_spikes(time_steps)