import inspect
import json
import random
import os
import pandas as pd
import torch
from torch import nn
import torch.nn.functional as F
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.Pitstop import Pitstop
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy


def a3c_choose_action(
    policy: nn.Module,
    h_c: tuple[torch.Tensor, torch.Tensor],
    state: UnifiedRaceState,
    state_tensor: torch.Tensor = None,
    device: str = "cpu",
) -> SimpleRaceStrategy:
    if state_tensor is None:
        state_tensor = state.to_tensor().to(device)

    logit, _, h_c = policy(
        state_tensor.unsqueeze(0).unsqueeze(0),
        h_c=h_c,
        device=device,
    )

    probs = F.softmax(logit.squeeze(0).squeeze(0), dim=-1)

    action = SimpleRaceStrategy(probs.multinomial(num_samples=1).detach().item())
    return action, h_c


def simple_strategy_epsilon_greedy_recurrent(
    epsilon: float,
    policy: nn.Module,
    hidden_state: torch.Tensor,
    state: UnifiedRaceState,
    state_tensor: torch.Tensor = None,
    filter_invalid_actions: bool = True,
    device: str = "cpu",
) -> tuple[SimpleRaceStrategy, SimpleRaceStrategy]:

    if state_tensor is None:
        state_tensor = state.to_tensor().to(device)

    with torch.no_grad():
        q_values, new_h = policy(
            x=state_tensor.unsqueeze(0).unsqueeze(0),
            h=hidden_state,
            device=device,
        )
        q_values = q_values.squeeze(0).squeeze(0)

    # Filter out invalid actions
    if filter_invalid_actions:
        safe_action_set = get_safe_action_set(state)
        q_values[safe_action_set == 0] = float("-inf")

    greedy_act = int(torch.argmax(q_values))
    greedy_strategy = SimpleRaceStrategy(greedy_act)

    # print(torch.round(q_values, decimals=4))

    if float(torch.rand(1)) > epsilon:
        return greedy_strategy, greedy_strategy, new_h
    else:
        valid_actions = [
            i for i in range(len(SimpleRaceStrategy)) if q_values[i] != float("-inf")
        ]
        chosen_strategy = SimpleRaceStrategy(random.choice(valid_actions))
        return chosen_strategy, greedy_strategy, new_h


def simple_strategy_epsilon_greedy(
    epsilon: float,
    policy: nn.Module,
    state: UnifiedRaceState,
    state_tensor: torch.Tensor = None,
    filter_invalid_actions: bool = True,
    device: str = "cpu",
) -> tuple[SimpleRaceStrategy, SimpleRaceStrategy]:
    if state_tensor is None:
        state_tensor = state.to_tensor().to(device)

    with torch.no_grad():
        q_values = policy(state_tensor, device)

    # Filter out invalid actions
    if filter_invalid_actions:
        safe_action_set = get_safe_action_set(state)
        q_values[safe_action_set == 0] = float("-inf")

    greedy_act = int(torch.argmax(q_values))
    greedy_strategy = SimpleRaceStrategy(greedy_act)

    # print(torch.round(q_values, decimals=4))

    if float(torch.rand(1)) > epsilon:
        return greedy_strategy, greedy_strategy
    else:
        valid_actions = [
            i for i in range(len(SimpleRaceStrategy)) if q_values[i] != float("-inf")
        ]
        chosen_strategy = SimpleRaceStrategy(random.choice(valid_actions))
        return chosen_strategy, greedy_strategy


def is_invalid_action(action: SimpleRaceStrategy, state: UnifiedRaceState) -> bool:
    return get_safe_action_set(state)[action.value] == 0


def get_safe_action_set(state: UnifiedRaceState) -> torch.tensor:
    safe_set = torch.tensor([1, 0, 0, 0])

    # Add the available pit options to the safe set
    if state.soft_available:
        safe_set[1] = 1
    if state.medium_available:
        safe_set[2] = 1
    if state.hard_available:
        safe_set[3] = 1

    # If the agent hits the terminal state and it is not finished, remove the NO_PIT strategy
    if state.terminal and not state.valid_finish:
        safe_set[0] = 0

    return safe_set


def hard_update(
    source_network: nn.Module,
    target_network: nn.Module,
) -> None:
    target_network.load_state_dict(source_network.state_dict())


def soft_update(
    source_network: nn.Module,
    target_network: nn.Module,
    tau: float,
) -> None:
    if tau == 1.0:
        hard_update(source_network, target_network)
        return

    target_sd = target_network.state_dict()
    source_sd = source_network.state_dict()
    for key in source_sd:
        target_sd[key] = (source_sd[key] * tau) + (target_sd[key] * (1.0 - tau))
    target_network.load_state_dict(target_sd)


def add_gaussian_noise(
    tensor: torch.Tensor,
    mean: float = 0.0,
    std: float = 0.01,
) -> torch.Tensor:
    """
    Add Gaussian noise to a PyTorch tensor.

    Args:
        tensor (torch.Tensor): Input tensor.
        mean (float): Mean of the Gaussian noise distribution.
        std (float): Standard deviation of the Gaussian noise distribution.

    Returns:
        torch.Tensor: Tensor with Gaussian noise added.
    """
    # Generate Gaussian noise with the same shape as the input tensor
    noise = torch.randn_like(tensor) * std + mean

    # Add the noise to the input tensor
    noisy_tensor = tensor + noise

    return noisy_tensor


def create_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_json(
    data: dict[str, any],
    file_name: str,
) -> None:
    with open(file_name + ".json", "w") as f:
        json.dump(data, f, indent=4)