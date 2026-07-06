# Football Match Analytics Dashboard - Nepal

A comprehensive, professional-grade football match analytics dashboard focused on the top football clubs in Nepal. This project was designed and developed for a University Software Engineering and Data Analytics module.

## 🚀 Features

*   **Interactive Dashboard:** High-level summary of league statistics, top goal scorers, and recent matches.
*   **Club Profiles:** Detailed overview of team statistics, history, and stadium information.
*   **Player Analytics:** Directory of players with performance tracking and ratings.
*   **Machine Learning Predictions:** Scikit-learn powered Random Forest model to forecast match outcomes.
*   **Data Visualizations:** Dynamic Matplotlib and Seaborn charts analyzing league goals, points, and trends.

## 🛠️ Technology Stack

*   **Backend:** Python 3, Flask
*   **Data Engineering:** Pandas, NumPy
*   **Machine Learning:** Scikit-Learn
*   **Visualization:** Matplotlib, Seaborn
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5

## 👥 Project Team

| Name | Role | Responsibilities | GitHub Branch |
| :--- | :--- | :--- | :--- |
| **Jesis** | Data Engineer | Datasets, Pandas loader, Preprocessing scripts | `jesis-data-engineer` |
| **Bishal** | System Designer | Flask Architecture, MVC Models, Frontend Templates, ML Engine | `bishal-system-designer` |
| **Sahid** | Analytical Validator | Validation, Unit Testing, QA | `sahid-analytical-validator` |
| **Aditya** | Documentation Lead | Documentation, DevOps, Trello Board, GitHub Workflow | `aditya-documentation` |

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd football-match-analytics-dashboard
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   Windows: `venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run Preprocessing Script:**
    This generates the required processed datasets inside `data/processed`.
    ```bash
    python -m app.services.preprocessing
    ```

6.  **Run the Flask Application:**
    ```bash
    python run.py
    ```

7.  **Access the application:** Open `http://127.0.0.1:5000` in your web browser.

## 🧪 Testing

To run the unit test suites:
```bash
python -m unittest discover -s tests
```

## 📂 Project Structure
See `docs/user_manual.md` for a full breakdown.
