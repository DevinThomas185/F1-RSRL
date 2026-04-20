from collections import deque
import random


class ReplayBuffer:
    def __init__(
        self,
        capacity: int,
    ):
        self.buffer = deque([], maxlen=capacity)

    def push(
        self,
        transition,
    ):
        self.buffer.append(transition)
        return self.buffer

    def push_list(
        self,
        transitions,
    ):
        self.buffer.extend(transitions)
        return self.buffer

    def sample(
        self,
        batch_size: int,
    ):
        return random.sample(self.buffer, batch_size)

    def __len__(self) -> int:
        return len(self.buffer)
