"""Compare simple one-step time-series baselines without fitting a model."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

DEMO_VALUES = [
    18.2, 18.5, 18.1, 19.0, 19.4, 19.1, 20.0, 20.3, 19.8, 20.6, 21.0, 20.7,
    21.4, 21.6, 21.1, 22.0, 22.3, 21.9, 22.4, 22.8, 22.1, 23.0, 23.2, 22.7,
]


def load_values(input_path: Path) -> list[float]:
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if "temperature_c" not in (reader.fieldnames or []):
            raise ValueError("CSV must contain a temperature_c column.")
        values = []
        for row_number, row in enumerate(reader, start=2):
            try:
                values.append(float(row["temperature_c"]))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid temperature on CSV row {row_number}.") from exc
    if len(values) < 2:
        raise ValueError("At least two ordered observations are required.")
    return values


def evaluate(values: list[float], window: int, min_history: int) -> dict[str, float | int]:
    if window < 1 or min_history < 1:
        raise ValueError("Window and minimum history must be positive.")
    if len(values) <= min_history:
        raise ValueError("The series must contain evaluation rows after minimum history.")
    naive_errors = []
    average_errors = []
    for index in range(min_history, len(values)):
        history = values[max(0, index - window) : index]
        actual = values[index]
        naive_errors.append(abs(actual - values[index - 1]))
        average_errors.append(abs(actual - (sum(history) / len(history))))
    return {
        "evaluation_points": len(naive_errors),
        "naive_mae": sum(naive_errors) / len(naive_errors),
        "moving_average_mae": sum(average_errors) / len(average_errors),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare simple one-step baselines.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="CSV file with temperature_c")
    source.add_argument("--demo", action="store_true", help="Use the synthetic in-source series")
    parser.add_argument("--window", type=int, default=3)
    parser.add_argument("--min-history", type=int, default=4)
    args = parser.parse_args()
    try:
        values = DEMO_VALUES if args.demo else load_values(args.input)
        result = evaluate(values, args.window, args.min_history)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Evaluation points: {result['evaluation_points']}")
    print(f"Naive MAE: {result['naive_mae']:.3f} C")
    print(f"Trailing mean MAE: {result['moving_average_mae']:.3f} C")
    print("No model was trained; baselines use only prior observations.")


if __name__ == "__main__":
    main()
