import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, Manager

import pandas as pd

from Classes.RaceStrategy.Pitstop import Pitstop
from Models.DRQNModel import DRQNModel
from Models.RandomFixedStrategyModel import RandomFixedStrategyModel
import Models.model_utilities as utils
from confidential.MercedesRSTranslator import MercedesRSTranslator
from Classes.RaceStrategy.BlankRaceStrategy import BlankRaceStrategy
from Classes.Enums import Track, TrackDetails, TyreCompound
from Classes.Errors import (
    BaseSimulationError,
    SimulationStuckError,
    SafetyCarDeployedError,
    InvalidActionError,
    PitstopNotAppliedError,
    LapAlreadyCompleteError,
)

from Models.StrategyRLModel import StrategyRLModel
from Models.MercedesLinearModel import MercedesLinearModel
from Models.FixedStrategyModel import FixedStrategyModel
from Testing.testing_results_utilities import (
    WorkerResults,
    Result,
    convert_pitstop_list_to_string,
)
from plotting import plot_race_histograms, plot_tyre_strategies

from termcolor import colored


def write_results_to_file(
    results: list[WorkerResults],
    results_file: str,
) -> None:
    results_file = results_file + ".csv"
    if not os.path.exists(results_file):
        test_run = 0
        with open(results_file, "w") as f:
            f.write("Test Run,Model Name,Track,Total Laps,Year,Finishing Position,Tyre Strategy\n")
    else:
        test_run = pd.read_csv(results_file)["Test Run"].max() + 1

    with open(results_file, "a") as f:
        for worker_results in results:
            for result in worker_results.results:
                f.write(
                    f"{test_run},{worker_results.model_name},{result.track},{result.total_laps},{result.year},{result.finishing_position},{convert_pitstop_list_to_string(result.tyre_strategy)}\n"
                )


def __main(
    models: list[StrategyRLModel],
    num_tests: int,
    allowed_years: list[str],
    allowed_tracks: list[Track],
    seed: int,
    disable_safety_car: bool,
    verbose: bool,
    plot_histograms: bool,
    plot_strategies: bool,
):
    with Manager() as manager:
        # Use a Manager to create a shared list for results
        results = manager.list()
        race_details = manager.list()

        # Initialize a worker for each model
        workers = []
        for model_id, model in enumerate(models):
            worker = Process(
                target=model_worker,
                args=(
                    model_id,
                    model,
                    num_tests,
                    results,
                    race_details,
                    seed,
                    disable_safety_car,
                    allowed_years,
                    allowed_tracks,
                    verbose,
                ),
            )
            workers.append(worker)
            worker.start()

        # Wait for all workers to finish
        for worker in workers:
            worker.join()

        #############################################################################
        # Save results to csv file
        #############################################################################
        write_results_to_file(results, "test_model_results")

        #############################################################################
        # Generate histograms for each model demonstrating average finishing position
        #############################################################################
        if plot_histograms:
            plot_race_histograms(results)

        #############################################################################
        # Plot tyre strategies
        #############################################################################
        if plot_strategies:
            plot_tyre_strategies(num_tests, results, race_details)

    return 0


def print_test_result(
    test_number: int,
    num_tests: int,
    model_name: str,
    message: str,
    track: Track,
    colour: str = "white",
) -> None:
    print(
        colored(
            f"{model_name:<50} | Test {test_number:<3} / {num_tests} | {track:<15} | {message}",
            colour,
        )
    )


def model_worker(
    model_id: int,
    model: StrategyRLModel,
    num_tests: int,
    results: list,
    race_details: list,
    seed: int,
    disable_safety_car: bool,
    allowed_years: list[str],
    allowed_tracks: list[Track],
    verbose: bool,
):
    worker_results = WorkerResults(model.name, [])
    np.random.seed(seed)

    while worker_results.get_num_results() < num_tests:
        test_number = worker_results.get_num_results() + 1
        test_failed = False
        simulator_at_fault = False
        step_size = 1

        sim_seed = np.random.randint(0, 1_000_000)
        sim = MercedesRSTranslator(
            selected_driver=model.selected_driver,
            seed=sim_seed,
            allowed_years=allowed_years,
            allowed_tracks=allowed_tracks,
            disable_safety_car=disable_safety_car,
            verbose=verbose,
        )
        track_details, state = sim.initialise_random_simulation()

        # If first thread then add the race details
        if model_id == 0:
            race_details.append(track_details)

        #### Prerequisites per model

        # If we are using the Mercedes Linear Model, we simulate the whole race
        # in one, otherwise we simulate one step at a time
        if isinstance(model, MercedesLinearModel):
            step_size = 100

        # If we are using the DRQN Model, we need to reset the hidden state
        if isinstance(model, DRQNModel):
            model.reset_h()

        # Generate a random strategy for the RandomFixedStrategyModel
        if isinstance(model, RandomFixedStrategyModel):
            model.generate_random_strategy(track_details.Track)

        #### Run the simulation
        while not state.terminal:
            try:
                action = model.predict(state)
                state = sim.step(step=step_size, strategy=action)
            except BaseSimulationError as e:
                if isinstance(e, SimulationStuckError):
                    msg = f"SIMULATION STUCK - L{e.lap_number}"
                if isinstance(e, SafetyCarDeployedError):
                    msg = f"SAFETY CAR DEPLOYED - {e.num_fsc_laps} FSC, {e.num_vsc_laps} VSC"
                elif isinstance(e, InvalidActionError):
                    msg = f"INVALID ACTION - {e.type}"
                elif isinstance(e, PitstopNotAppliedError):
                    msg = f"PITSTOP NOT APPLIED - L{e.lap_number:.2f}"
                elif isinstance(e, LapAlreadyCompleteError):
                    msg = f"LAP ALREADY COMPLETED - L{e.lap_number:.2f} "
                elif isinstance(e, Exception):
                    msg = f"UNKNOWN ERROR"
                test_failed = True
                simulator_at_fault = e.simulator_at_fault
                break

        # If the test failed and the simulator was at fault
        if test_failed and simulator_at_fault:
            print_test_result(
                test_number, num_tests, model.name, msg, sim.get_track(), "red"
            )
            continue

        # Otherwise, we have either a valid result, or a failure due to the model
        finishing_position = sim.get_finishing_position(driver=model.selected_driver)
        pitstops = sim.get_pitstops(driver=model.selected_driver)

        worker_results.results.append(
            Result(
                track_details.Track,
                track_details.TotalLaps,
                track_details.Year,
                finishing_position,
                pitstops,
            )
        )

        if test_failed and not simulator_at_fault:
            print_test_result(
                test_number, num_tests, model.name, msg, sim.get_track(), "yellow"
            )

        if not test_failed:
            print_test_result(
                test_number,
                num_tests,
                model.name,
                f"P{finishing_position:<2} | {convert_pitstop_list_to_string(pitstops)}",
                sim.get_track(),
                "green",
            )

    results.append(worker_results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--num_tests",
        "-n",
        type=int,
        default=10,
        help="Number of tests to run",
    )

    parser.add_argument(
        "--with_mercedes",
        "-m",
        action="store_true",
        default=False,
        help="Whether to include the Mercedes model for comparison",
    )

    parser.add_argument(
        "--with_fixed",
        "-f",
        action="store_true",
        default=False,
        help="Whether to include the Fixed Strategy model for comparison",
    )

    parser.add_argument(
        "--with_random_fixed",
        "-r",
        action="store_true",
        default=False,
        help="Whether to include the Random Fixed Strategy model for comparison",
    )

    parser.add_argument(
        "--models",
        nargs="*",
        default=[],
        help="List of models to load",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Whether to print progress to stdout",
    )

    parser.add_argument(
        "--years",
        "-y",
        nargs="+",
        default=[],
        help="List of years to allow",
    )

    parser.add_argument(
        "--tracks",
        "-t",
        nargs="+",
        default=[],
        help="List of tracks to allow",
    )

    parser.add_argument(
        "--seed",
        "-s",
        type=int,
        default=np.random.randint(0, 1_000_000),
        help="Seed for random number generation",
    )

    parser.add_argument(
        "--disable_safety_car",
        "-d",
        action="store_true",
        default=False,
        help="Whether to disable the safety car in simulations",
    )

    parser.add_argument(
        "--plot_histograms",
        "-ph",
        action="store_true",
        default=False,
        help="Whether to plot histograms of the results",
    )

    parser.add_argument(
        "--plot_strategies",
        "-ps",
        action="store_true",
        default=False,
        help="Whether to plot the tyre strategies",
    )

    args = parser.parse_args()

    # For all models, select only the ones with the .pth extension
    models = [
        model
        for model in args.models
        if model.endswith(".pth") and not model.endswith("optimiser_state.pth")
    ]
    models = [StrategyRLModel.load_model(model) for model in models]

    if args.with_mercedes:
        models.append(MercedesLinearModel(selected_driver=44))

    if args.with_fixed:
        models.append(FixedStrategyModel(selected_driver=44))

    if args.with_random_fixed:
        models.append(RandomFixedStrategyModel(selected_driver=44))

    if len(models) == 0:
        raise ValueError("Must provide at least one model to test")

    sys.exit(
        __main(
            models=models,
            num_tests=args.num_tests,
            allowed_years=args.years,
            allowed_tracks=[Track[track] for track in args.tracks],
            seed=args.seed,
            disable_safety_car=args.disable_safety_car,
            verbose=args.verbose,
            plot_histograms=args.plot_histograms,
            plot_strategies=args.plot_strategies,
        )
    )
