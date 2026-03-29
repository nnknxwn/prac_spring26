import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Dataset:
    equations: List[str]
    boundary_conditions: List[str]
    variables: List[str]
    t_var: str
    a: float
    b: float
    t_star: float
    p0: List[float]
    inner_method: str = "RK45"
    inner_rtol: float = 1e-6
    inner_atol: float = 1e-6
    outer_method: str = "RK45"
    outer_rtol: float = 1e-4
    outer_atol: float = 1e-4
    max_iter: int = 10


def save(dataset: Dataset, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(dataset), f, indent=2, ensure_ascii=False)


def load(path: str) -> Dataset:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Dataset(**data)
