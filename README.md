# A/B Test Sequential Analysis

A complete statistical framework for A/B testing that solves the "peeking problem" using Sequential Probability Ratio Test (SPRT). This project demonstrates why traditional frequent peeking at p-values leads to false positives and provides a robust solution through sequential testing.

## Features

- **Sequential Testing Implementation**: Full SPRT (Sequential Probability Ratio Test) implementation with configurable decision boundaries
- **Interactive Dashboard**: Real-time Streamlit dashboard for monitoring A/B tests with visualization of test statistics
- **Peeking Problem Simulation**: Comprehensive notebooks demonstrating the dangers of multiple hypothesis testing
- **Production-Ready**: Clean, modular codebase with proper data ingestion and statistical calculations

## Project Structure

```
google_query_dataset/
├── .env                      # Environment variables (DATA_PATH)
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/                     # CSV data files (gitignored)
│   └── ab_test_data-*.csv
├── notebooks/                # Analysis and simulations
│   └── simulation.ipynb      # "Peeking problem" demonstration
└── src/                      # Production code
    ├── app.py                # Streamlit dashboard
    └── statistics.py         # SPRT statistical engine
```

## Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd google_query_dataset
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure your data path in `.env`:
```
DATA_PATH=data/ab_test_data-000000000000.csv
```

## Usage

### Run the Interactive Dashboard
Launch the Streamlit dashboard to monitor A/B tests in real-time:
```bash
streamlit run src/app.py
```

The dashboard provides:
- Real-time test statistics and decision boundaries
- Visual representation of sequential test progress
- Automatic stopping recommendations based on SPRT

### Explore the Simulations
Run the Jupyter notebook to see demonstrations of the peeking problem:
```bash
jupyter notebook notebooks/simulation.ipynb
```

The notebook includes:
- A/A test simulations showing false positive rates
- Visualization of p-value fluctuation over time
- Comparison between traditional and sequential testing

## How It Works

### The Peeking Problem
Traditional A/B testing requires choosing a sample size upfront and checking results only once. Repeatedly checking p-values (peeking) inflates the false positive rate far beyond the nominal significance level.

### SPRT Solution
Sequential Probability Ratio Test allows continuous monitoring while maintaining statistical validity:
- Calculates log likelihood ratios at each observation
- Uses predefined decision boundaries (α and β thresholds)
- Stops early when sufficient evidence is gathered
- Controls Type I and Type II error rates

## Project Components

### `src/statistics.py`
Core SPRT implementation with functions for:
- Log likelihood ratio calculation
- Decision boundary computation
- Statistical test evaluation

### `src/app.py`
Streamlit dashboard providing:
- Interactive parameter configuration
- Real-time visualization of test progress
- Decision recommendations

### `notebooks/simulation.ipynb`
Educational demonstrations including:
- Data ingestion and cleaning from GA4 events
- Simulation of the peeking problem
- Comparative analysis of testing methodologies

## Requirements

- Python 3.8+
- pandas, numpy, scipy for data processing and statistics
- streamlit, plotly for interactive visualization
- jupyter for notebooks

See `requirements.txt` for complete dependency list.

## License

This project is available for educational and research purposes.
