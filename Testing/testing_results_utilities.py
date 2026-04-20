from typing import NamedTuple

import numpy as np
import pandas as pd

from Classes.Enums import Track, TyreCompound
from Classes.RaceStrategy.Pitstop import Pitstop


class Result(NamedTuple):
    track: Track
    total_laps: int
    year: int
    finishing_position: int
    tyre_strategy: list[Pitstop]


class WorkerResults(NamedTuple):
    model_name: str
    results: list[Result]

    def get_num_results(self) -> int:
        return len(self.results)
    


def convert_pitstop_list_to_string(
    pitstop_list: list[Pitstop],
) -> str:
    return "".join(
        [
            f"{str(pitstop.get_tyre_compound())[0]}{pitstop.get_lap():<2}"
            for pitstop in pitstop_list
        ]
    )


def convert_string_to_pitstop_list(
    pitstop_string: str,
) -> list[Pitstop]:
    pitstop_list = []
    for i in range(0, len(pitstop_string), 3):
        compound = TyreCompound.convert(pitstop_string[i])
        lap = int(pitstop_string[i + 1 : i + 3])
        pitstop = Pitstop(compound, lap)
        pitstop_list.append(pitstop)
    return pitstop_list

def convert_df_to_worker_results(
    df: pd.DataFrame,
) -> list[WorkerResults]:
    results: dict[str, list[Result]] = {}
    for _, row in df.iterrows():
        result = Result(
            track=row["Track"],
            year=row["Year"],
            total_laps=row["Total Laps"],
            finishing_position=row["Finishing Position"],
            tyre_strategy=convert_string_to_pitstop_list(row["Tyre Strategy"]),
        )
        if row["Model Name"] not in results:
            results[row["Model Name"]] = []

        results[row["Model Name"]].append(result)

    worker_results = []
    for model_name, model_results in results.items():
        worker_results.append(WorkerResults(model_name, model_results))
    
    return worker_results