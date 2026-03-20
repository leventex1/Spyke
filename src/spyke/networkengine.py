from collections import deque
from abc import ABC, abstractmethod


class QueueProcess(ABC):

    @abstractmethod
    def process(self, time_step: int) -> list["QueueProcess"]:
        pass

    @abstractmethod
    def is_primary_process(self) -> bool:
        pass


class NetworkEngine:

    def __init__(self):
        self.process_queue: deque[QueueProcess] = deque()
        self.time_step = 0

    def add_process(self, queue_process: QueueProcess) -> None:
        if queue_process.is_primary_process():
            self.process_queue.appendleft(queue_process)
        else:
            self.process_queue.append(queue_process)

    def spin(self) -> None:
        next_queue: deque[QueueProcess] = deque()

        for queue_process in self.process_queue:
            queue_processes = queue_process.process(self.time_step)
            for result_queue_process in queue_processes:
                if result_queue_process.is_primary_process():
                    next_queue.appendleft(result_queue_process)
                else:
                    next_queue.append(result_queue_process)

        self.process_queue = next_queue
        self.time_step += 1

    def reset(self) -> None:
        self.process_queue.clear()
        self.time_step = 0