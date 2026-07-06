# API & Route Documentation

The Flask application architecture handles routes as view controllers.

### Core Routes

*   `GET /`
    *   **Controller:** `main.index`
    *   **Action:** Renders `index.html` injecting `dashboard_metrics`.
*   `GET /teams`
    *   **Controller:** `main.teams`
    *   **Action:** Renders `teams.html` injecting full club dictionaries.
*   `GET /players`
    *   **Controller:** `main.players`
    *   **Action:** Renders `players.html` injecting player statistics.
*   `GET /matches`
    *   **Controller:** `main.matches`
    *   **Action:** Renders `matches.html` injecting raw match timelines.
*   `GET /statistics`
    *   **Controller:** `main.statistics`
    *   **Action:** Renders `statistics.html`.
*   `GET /analytics`
    *   **Controller:** `main.analytics`
    *   **Action:** Renders `analytics.html`.
*   `GET /visualization`
    *   **Controller:** `main.visualization`
    *   **Action:** Triggers Matplotlib image generation and renders `visualization.html`.
*   `GET, POST /prediction`
    *   **Controller:** `main.prediction`
    *   **Action:** Handles form submission for team comparisons. Returns `prediction_result` dictionary upon POST.

### Internal Python Services API

*   `app.services.predictions.predict_match(home, away)` -> `dict`
*   `app.services.loader.load_matches(processed=True)` -> `pd.DataFrame`
*   `app.services.statistics.get_league_summary()` -> `dict`
