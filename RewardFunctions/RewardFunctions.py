from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.BaseRaceStrategy import BaseRaceStrategy
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from math import tanh

POSITION_REWARDS = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
}

ALT_POSITION_REWARDS = {
    1: 20,
    2: 19,
    3: 18,
    4: 17,
    5: 16,
    6: 15,
    7: 14,
    8: 13,
    9: 12,
    10: 11,
    11: 10,
    12: 9,
    13: 8,
    14: 7,
    15: 6,
    16: 5,
    17: 4,
    18: 3,
    19: 2,
    20: 1,
}

FAILURE_PENALTY = 1000


################################################################################
# Helper Functions
################################################################################
def is_invalid_action(
    state: UnifiedRaceState,
    action: BaseRaceStrategy,
):
    return (
        (not state.soft_available and action == SimpleRaceStrategy.PIT_SOFT)
        or (not state.medium_available and action == SimpleRaceStrategy.PIT_MEDIUM)
        or (not state.hard_available and action == SimpleRaceStrategy.PIT_HARD)
    )


def is_invalid_finish(
    next_state: UnifiedRaceState,
):
    return next_state.terminal and not next_state.valid_finish


def is_valid_finish(
    next_state: UnifiedRaceState,
):
    return (
        next_state.terminal
        and next_state.valid_finish
        and next_state.race_progress >= 0.97
    )


################################################################################
# Reward Functions
################################################################################


def gap_rewards(
    state: UnifiedRaceState,
    action: BaseRaceStrategy,
    next_state: UnifiedRaceState,
) -> float:
    """Reward function that rewards the model for minimising the gap to the leader"""

    reward = 0
    # If catching car ahead
    if next_state.gap_ahead < state.gap_ahead:
        reward += 1

    # If increasing on car behind
    if next_state.gap_behind > state.gap_behind:
        reward += 1

    # If decreasing gap to leader
    if next_state.gap_to_leader < state.gap_to_leader:
        reward += 1

    # Penalise invalid actions
    if is_invalid_action(state, action) or (
        next_state.terminal and not next_state.valid_finish
    ):
        return -FAILURE_PENALTY

    # Terminal Reward
    if is_valid_finish(next_state):
        return 100 * POSITION_REWARDS[next_state.position] - next_state.gap_to_leader

    return reward


def basic_reward(
    state: UnifiedRaceState,
    action: BaseRaceStrategy,
    next_state: UnifiedRaceState,
) -> float:

    last_positional_reward = -(25 / 361) * (state.position - 1) ** 2 + 25
    next_positional_reward = -(25 / 361) * (next_state.position - 1) ** 2 + 25

    if next_state.race_progress == 1.0:
        return 100 * POSITION_REWARDS[next_state.position]
    else:
        return next_positional_reward - last_positional_reward


def simple_reward(
    state: UnifiedRaceState,
    action: BaseRaceStrategy,
    next_state: UnifiedRaceState,
) -> float:
    """Simple reward function that rewards the model for finishing and negatively for failing"""

    if is_invalid_action(state, action) or is_invalid_finish(next_state):
        return 0 # -1

    if is_valid_finish(next_state):
        return 100 * POSITION_REWARDS[next_state.position] # ALT_POSITION_REWARDS[next_state.position]

    return 1 # 0


def stint_reward(
    state: UnifiedRaceState,
    action: BaseRaceStrategy,
    next_state: UnifiedRaceState,
) -> float:
    """Reward function that rewards the model for minimising reward functions whilst maximising the terminal reward"""

    if next_state.terminal and not next_state.valid_finish:
        return -FAILURE_PENALTY

    if is_invalid_action(state, action):
        return -FAILURE_PENALTY

    if (
        next_state.terminal
        and next_state.valid_finish
        and next_state.race_progress == 1.0
    ):
        return 100 * POSITION_REWARDS[next_state.position] - next_state.gap_to_leader

    return -1 / 100 * next_state.stint_length


def thomas_reward_2(
    state: UnifiedRaceState,
    action: BaseRaceStrategy,
    next_state: UnifiedRaceState,
) -> float:
    """
    This reward function does not use heuristics and reward shaping to guide the model.
    We reward the model on its final position, as well as penalise it for invalid actions.
    Additionally, for every step that the model cannot finish the race validly, it is penalised.
    Every other step is rewarded with a small positive reward.

    Args:
        state (UnifiedRaceState): Current state.
        action (BaseRaceStrategy): Action taken in the current state.
        next_state (UnifiedRaceState): State moved to.

    Returns:
        float: _description_
    """
    DEFAULT_REWARD = 1

    # Invalid action
    if is_invalid_action(state, action):
        return -FAILURE_PENALTY

    # Pitstop without valid finish
    if action != SimpleRaceStrategy.NO_PIT and not state.valid_finish:
        return DEFAULT_REWARD

    # Pitstop with valid finish
    if action != SimpleRaceStrategy.NO_PIT and state.valid_finish:
        return -10

    if (
        next_state.terminal
        and next_state.valid_finish
        and next_state.race_progress >= 0.97  # Should be race_progress == 1.0
    ):
        return 100 * POSITION_REWARDS[next_state.position]

    if next_state.terminal and not next_state.valid_finish:
        return -FAILURE_PENALTY

    return DEFAULT_REWARD


def thomas_reward(
    state: UnifiedRaceState,
    action: BaseRaceStrategy,
    next_state: UnifiedRaceState,
) -> float:
    """Designed reward function for the project. This reward function is designed
    to scale rewards based on their race progress to incentivise the agent to make
    decisions that are beneficial in the long term.

    Args:
        state (UnifiedRaceState): Current state.
        action (BaseRaceStrategy): Action taken in the current state.
        next_state (UnifiedRaceState): State moved to.

    Returns:
        float: The reward for the agent's action.
    """

    catastrophic_penalty_applied = False

    ############################# Positional reward ############################
    # The agent receives a reward for gaining positions without losing too many
    # from pitstops.
    # INCENTIVISES: Gaining positions without losing too many from pitstops

    positional_reward = (20 - next_state.position) / 19
    ############################################################################

    ########################### Gap to leader reward ###########################
    # The agent receives a reward for minimising the gap to the leader.
    # INCENTIVISES: Minimising the gap to the leader

    current_gap_to_leader = state.gap_to_leader
    next_gap_to_leader = next_state.gap_to_leader

    if next_gap_to_leader < current_gap_to_leader:
        gap_to_leader_reward = 1
    else:
        gap_to_leader_reward = 0
    ############################################################################

    ############################## Laptime reward ##############################
    # If the agent sets a faster laptime than their reference laptime, they
    # receive a reward. If they set a slower laptime, they receive a penalty.
    # INCENTIVISES: Setting faster lap times

    laptime_reward = -0.5 * tanh(50 * (next_state.last_lap_to_reference - 1)) + 0.5
    ############################################################################

    ############################ Stint length reward ###########################
    # The agent gets a negative reward for the duration of the stint.
    # INCENTIVISES: Not staying out too long

    stint_length_reward = -tanh(1 / 20 * (next_state.stint_length - 1)) + 1
    ############################################################################

    ########################## Invalid action penalty ##########################
    # If the agent attempts to pit for a tyre that is not available, they
    # receive a penalty for doing so.
    # INCENTIVISES: Valid pit decision within the available decisions

    invalid_action_penalty = 0
    if is_invalid_action(state, action):
        invalid_action_penalty = 1
        catastrophic_penalty_applied = True
    ############################################################################

    ################# Terminal state is invalid finish penalty #################
    # If the agent finishes the race but does so invalidly, they receive a
    # penalty for doing so.
    # INCENTIVISES: Valid finishes

    invalid_finish_penalty = 0
    if next_state.terminal and not next_state.valid_finish:
        invalid_finish_penalty = 1
        catastrophic_penalty_applied = True
    ############################################################################

    ############################ Terminality reward ############################
    # If the agent successfully finishes the race and does so validly, they
    # receive a reward based on their finishing position
    # INCENTIVISES: Higher finishing positions

    terminality_reward = 0
    if next_state.terminal and not catastrophic_penalty_applied:
        terminality_reward = (20 - next_state.position) / 19
        # POSITION_REWARDS[next_state.position]
    ############################################################################

    # Sum the rewards and penalties by their weights
    rewards = [
        (10, positional_reward),
        (10, gap_to_leader_reward),
        (0, laptime_reward),
        (0, stint_length_reward),
        (0, terminality_reward),
    ]

    penalties = [
        (100, invalid_action_penalty),
        (100, invalid_finish_penalty),
    ]

    # Weighted sum of the rewards and penalties
    reward = sum([w * r for w, r in rewards])
    penalty = sum([w * p for w, p in penalties])

    # Scale the reward based on the race progress from 0.5 to 1.0
    a = 0.5

    reward_scale = (1 - a) * next_state.race_progress + a
    penalty_scale = (1 - a) * (1 - next_state.race_progress) + a

    # for w, r in rewards:
    #     print(f"{w}*{round(r, 3)}", end="\t")
    # print()

    return reward_scale * reward - penalty_scale * penalty


def picinotti_reward(
    state: UnifiedRaceState,
    action: BaseRaceStrategy,
    next_state: UnifiedRaceState,
) -> float:
    tlap = next_state.last_lap_time
    tmax = next_state.reference_lap_time  # TODO: Ref is not max?
    return 1 - min(tlap, tmax) / tmax


def heilmeier_reward(
    state: UnifiedRaceState,
    action: BaseRaceStrategy,
    next_state: UnifiedRaceState,
) -> float:
    position_gain_reward = state.position - next_state.position
    laptime_reward = next_state.reference_lap_time - next_state.last_lap_time

    return max(5 * position_gain_reward + laptime_reward, 0)
