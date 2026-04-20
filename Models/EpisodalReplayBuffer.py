from collections import deque
import random


class EpisodalReplayBuffer:
    __slots__ = [
        "__buffer",
        "__current_episode",
    ]

    def __init__(
        self,
        episode_capacity: int,
    ):
        self.__current_episode = []
        self.__buffer = deque([], maxlen=episode_capacity)

    def delete_current_episode(self):
        self.__current_episode = []

    def store_current_episode(self):
        if len(self.__current_episode) > 1:
            self.__buffer.append(self.__current_episode)
        self.delete_current_episode()

    def get_current_episode(self):
        return self.__current_episode

    def get_current_episode_states(self):
        return [transition[0] for transition in self.__current_episode]

    def push(
        self,
        transition,
    ):
        self.__current_episode.append(transition)
        return self.__buffer

    def remove_last_transition(
        self,
    ):
        self.__current_episode = self.__current_episode[:-1]

    def sample(
        self,
    ):
        return random.sample(self.__buffer, 1)[0]

    def __len__(self) -> int:
        return len(self.__buffer)
