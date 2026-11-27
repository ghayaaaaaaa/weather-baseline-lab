# Weather Baseline Lab

A small Python CLI that compares two transparent one-step forecasting baselines on a time series: previous-value (naive) and trailing moving average. It reports mean absolute error over the evaluated rows.

## Run

Use Python 3.11 or newer from this directory:

```bash
python -m weather_baseline --demo --window 3 --min-history 4
python -m weather_baseline --input path/to/series.csv --window 3 --min-history 4
```

The CSV requires one numeric `temperature_c` column in chronological order.

## Method

For each evaluation point, both methods use only earlier values. The naive forecast repeats the previous observation. The moving-average forecast averages up to the requested number of recent observations. Both methods use the same evaluation range.

## Data and limitations

The demonstration series is synthetic and stored in source. This AI-assisted portfolio demo is inspired by a weather-forecasting theme in a folder supplied by Ghaya; no original data, checkpoints, model weights, or notebook outputs are included. This is not a live forecast. No model is trained or tuned, and no accuracy claim is made. No open-source license is included.
