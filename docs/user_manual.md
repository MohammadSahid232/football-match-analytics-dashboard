# User Manual: Football Match Analytics Dashboard

Welcome to the user manual for the Nepal Football Analytics Dashboard. This guide will help you navigate the system.

## 1. Dashboard Overview
Upon starting the application and navigating to `http://127.0.0.1:5000`, you land on the Dashboard.
- **Top Metrics:** View total matches, goals, average goals, and active players.
- **Top Standings:** A quick preview of the top 5 clubs in the league.
- **Recent Matches:** History of the latest 5 matches played in the simulated dataset.

## 2. Clubs and Players
- Navigate to **Clubs** to view details about all 10 registered Nepal teams, including stadium and manager data.
- Navigate to **Players** to view the comprehensive roster. You can analyze their performance rating, which is dynamically color-coded.

## 3. Deep Analytics and Statistics
- **Statistics:** Shows the full league standings alongside the Golden Boot and Playmaker leaderboards.
- **Deep Analytics:** Explore contextual statistics like home win rates, clean sheets, and average possession per team.

## 4. Machine Learning Predictions
- Navigate to **ML Prediction**.
- Select a Home Team and an Away Team from the dropdown menus.
- Click **Predict Outcome**.
- The system will process historical match logic through a Random Forest Classifier and return the probability percentages for a Home Win, Draw, or Away Win.

## 5. Visualizations
- View automatically generated charts under the **Visualizations** tab.
- Includes Goal distributions and points summaries generated via Matplotlib.
