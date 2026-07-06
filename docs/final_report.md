# Final Project Report: Football Match Analytics Dashboard

## 1. Executive Summary
This report summarizes the design, development, and implementation of the Nepal Football Match Analytics Dashboard. Developed over several collaborative sprints simulated via Git branches, the project utilizes data engineering, backend architecture, unit testing, and machine learning.

## 2. Architecture and Design
The system employs the Model-View-Controller (MVC) architecture standard adapted for Flask:
- **Models:** Abstracted `Team`, `Player`, and `Match` objects.
- **Views:** Jinja2 templated HTML files stylized with Bootstrap 5.
- **Controllers:** Flask Blueprints routing logic.
- **Data Layer:** Pandas DataFrames interfacing with CSV datasets.

## 3. Data Engineering (Jesis)
Raw data containing 10 teams, 50 players, and 30 matches was manually constructed to replicate the Nepalese football league. Preprocessing pipelines were developed to impute missing values, handle datatypes, and guarantee data integrity before analysis.

## 4. System Implementation & ML (Bishal)
The core Flask engine processes analytical statistics dynamically. A key feature is the Match Prediction engine, built using Scikit-Learn's `RandomForestClassifier`. The model analyzes the offensive and defensive capabilities (average goals scored/conceded) of the home and away teams to generate outcome probabilities.

## 5. Testing & Validation (Sahid)
Six extensive unit test suites were developed using Python's `unittest` module. Testing verified:
- DataFrame structural integrity.
- Preprocessing transformation accuracy.
- Probabilistic boundary logic (ensuring probabilities sum to 100%).
- Routing accessibility (HTTP 200 checks).

## 6. Conclusion
The dashboard successfully fulfills the requirements of a comprehensive university-level software engineering and data analytics project, proving the efficacy of modular programming and strict Git workflow adherence.
