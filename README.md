# FIFA World Cup 2026 Data Analytics Module

A comprehensive, professional-grade football match analytics pipeline focused on the FIFA World Cup 2026. This project covers raw simulated tournament data generation, automated cleaning, feature engineering, exploratory data analysis (EDA), and 8 high-resolution dark-themed analytical visualizations.

---

## 🚀 Key Modules & Capabilities

- **Realistic Data Simulation:** Simulates matches using ELO-based Poisson distributions, generating match event stats (scores, possession, xG, cards, attendance) for all 48 qualified countries and 104 matches.
- **Robust Data Cleaning:** Pipeline that standardizes string formats, imputes missing values (median/mode), clips goal values, and removes extreme statistical outliers.
- **Feature Engineering:** Preprocessing that generates custom columns like `total_goals`, `goal_diff`, `is_draw`, `goals_per_90`, `efficiency_score`, aggregates statistics across matches, and scales features for machine learning models.
- **Exploratory Data Analysis (EDA):** Modular services that generate tournament summaries, identify top scorers/assisters, calculate attendance metrics, and construct feature correlation matrices.
- **Data Visualizations:** Generates 8 dark-theme Matplotlib/Seaborn charts saved to static assets.

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd football-match-analytics-dashboard
   ```

2. **Activate the Virtual Environment:**
   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📊 How to Run the Analytics Pipeline

You can run each stage of the pipeline directly from the command line:

### 1. (Optional) Re-Generate Raw Datasets
This script generates the 4 raw tournament datasets inside `data/raw/fifa2026/`:
```bash
python generate_fifa2026_data.py
```

### 2. Run the Data Cleaning Pipeline
This reads the raw datasets, applies the cleaning rules, and saves the cleaned results to `data/processed/fifa2026/`:
```bash
python -m app.services.fifa2026_cleaning
```

### 3. Run Preprocessing & Feature Engineering
This generates custom performance metrics, scales data, and outputs DataFrame summaries:
```bash
python -m app.services.fifa2026_preprocessing
```

### 4. Generate Visualizations (8 charts)
This generates the analytical charts and saves them directly to `static/images/fifa2026/`:
```bash
python -m app.services.fifa2026_visualization
```

---

## 🧪 Testing

We use Python's built-in `unittest` framework to execute the testing pipeline. To run all 21 unit tests (covering loading, cleaning, feature calculations, and EDA functions):

```bash
python -m unittest discover -s tests
```

---

## 📂 File Structure

```
football-match-analytics-dashboard/
│
├── app/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       ├── fifa2026_loader.py         # Loads raw and cleaned CSVs
│       ├── fifa2026_cleaning.py       # Data cleaning and filtering
│       ├── fifa2026_preprocessing.py  # Feature engineering & scaling
│       ├── fifa2026_eda.py            # Summary analytics & statistics
│       └── fifa2026_visualization.py  # Matplotlib/Seaborn charts
│
├── data/
│   ├── raw/fifa2026/                  # Raw CSV files
│   └── processed/fifa2026/            # Cleaned CSV files
│
├── static/
│   └── images/fifa2026/               # 8 generated PNG charts
│
├── tests/
│   ├── test_fifa2026_cleaning.py      # Cleaning unit tests
│   ├── test_fifa2026_preprocessing.py # Preprocessing unit tests
│   └── test_fifa2026_eda.py           # EDA metrics unit tests
│
├── generate_fifa2026_data.py          # Data simulator
└── requirements.txt
```
