[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fzgrxvujrbs8oipfexg6vb.streamlit.app/)

# Case Study: Solving the A/B Testing Peeking Problem with SPRT

## 📊 Executive Summary
Traditional A/B testing methodology breaks when teams check results repeatedly ("peeking"), intentionally or unintentionally inflating false positive rates from 5% to over 15%. To address this, I built an interactive dashboard using the Sequential Probability Ratio Test (SPRT). This solution enables continuous monitoring while maintaining statistical validity, reducing false positives by 67% and detecting true winners 30% faster with 40% fewer samples required.

## 🎯 The Problem: The Hidden Cost of Peeking

### What is Peeking?
In traditional frequentist A/B testing, teams are statistically required to:
1. Pre-define a sample size.
2. Collect all data.
3. Check results exactly ONCE at the end.

In reality, stakeholders check dashboards daily, asking, "Is it significant yet?"

### Why This Matters
Through a simulation of 1,000 A/A tests (where both groups were identical), I demonstrated the statistical breakdown:
* **Traditional Testing (No Peeking):** False Positive Rate of 4.2% (Close to the expected 5% alpha).
* **Traditional Testing (With Peeking):** Checking just 6 times increased the False Positive Rate to 15.6%.

### Business Impact
* **1 in 6 "winning" variants are actually false positives.**
* Engineering resources are wasted implementing ineffective changes.
* Revenue is lost by shipping features that do not actually improve metrics.

## 💡 The Solution: Sequential Probability Ratio Test (SPRT)

### How SPRT Works
Unlike traditional T-tests or Z-tests which require a fixed sample size, SPRT evaluates data as it arrives.
1. It calculates a **log likelihood ratio** at each new observation step.
2. It compares this ratio against pre-defined **decision boundaries** (Upper and Lower thresholds).
3. The test stops immediately once a boundary is crossed.

### Key Innovation
* Traditional testing asks: "Did we collect enough data?"
* SPRT asks: "Do we have enough *evidence*?"

This fundamental shift allows for continuous monitoring without the statistical penalty associated with peeking.

## 📈 Results & Impact

I validated the SPRT implementation against traditional testing using simulations on real Google Analytics e-commerce data (93,612 users, 1.14% conversion rate).

### Simulation Results (1,000 A/A tests each)

| Metric | Traditional (No Peek) | Traditional (Peeking 6x) | SPRT (Continuous) |
|--------|----------------------|--------------------------|-------------------|
| **False Positive Rate** | 4.2% | 15.6% | **5.1%** ✅ |
| **Average Sample Size** | 60,000 | 60,000 | **36,000** (40% reduction) |
| **Time to Decision** | 30 days | 30 days | **21 days** (30% faster) |

### Key Findings
1. **Maintains Statistical Validity:** The SPRT method kept the error rate near the target 5%, whereas peeking inflated it by 3x. This represents a **67% reduction in false positives**.
2. **Faster Decisions:** The average stopping point was Step 180 of 300. This translates to a **30% faster time-to-decision**, allowing true winners to be shipped earlier.
3. **Efficiency:** The **40% reduction** in required sample size reduces the "opportunity cost" of testing, allowing for faster iteration cycles.

## 🔧 Technical Implementation

### Architecture
`Data Pipeline` → `SPRT Engine` → `Interactive Dashboard` → `Export`

### Core Components
* **Statistical Engine (Python/SciPy):** Implemented the SPRT class with configurable alpha, beta, and Minimum Detectable Effect (MDE). I handled edge cases, such as 0% conversion rates, using Laplace smoothing to prevent numerical errors in log calculations.
* **Sequential Analysis:** Built logic to process time-ordered data, calculating cumulative sums and Log Likelihood Ratios (LLR) at specific steps (e.g., every 100 users).
* **Visualization (Plotly/Streamlit):** Developed a real-time dashboard plotting the LLR against dynamic Upper and Lower decision boundaries.

## 💭 Key Learnings

* **Statistical Rigor:** Understanding the underlying math (Wald's SPRT formulation) was crucial for handling edge cases in code correctly.
* **Cost of Errors:** I realized that Type I errors (False Positives) are often more expensive than running tests longer because they lead to permanent implementation of bad ideas.
* **Communication:** Advanced statistics are useless if stakeholders don't trust them. The dashboard was essential to bridge the gap between the math and the decision-makers.

---

## 🛠️ Installation & Usage

### Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd google_query_dataset

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

Demo Feature: Once the app is running, check the "Simulate Artificial Lift" box in the sidebar. This injects a synthetic 15% conversion lift into Group B, allowing you to instantly visualize how the SPRT algorithm detects a winner and triggers the Revenue Impact Analysis.

The dashboard provides:
- Real-time test statistics and decision boundaries
- Visual representation of sequential test progress
- Automatic stopping recommendations based on SPRT

### Explore the Simulations
Run the Jupyter notebook to see demonstrations of the peeking problem:
```bash
jupyter notebook notebooks/simulation.ipynb
```

### Project Structure
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


## License

This project is available for educational and research purposes.
