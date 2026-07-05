# Football Match Analytics Dashboard - Trello Kanban Board

This document represents the project's Trello board, including roles, estimates, labels, and due dates across the phases.

## Team Members
* **Jesis** (Data Engineer - `jesis-data-engineer`)
* **Sahid** (Analytical Validator - `sahid-analytical-validator`)
* **Bishal** (System Designer - `bishal-system-designer`)
* **Aditya** (Documentation Lead - `aditya-documentation`)

---

## Column: Project Planning

### Card 01: Project Scope Definition & Initialization
* **Description**: Define core project deliverables, technology stack requirements, and establish the main Git repository.
* **Checklist**:
  - [x] Create project plan & architecture diagram
  - [x] Initialize Git repository
  - [x] Create initial branches
* **Priority**: Critical
* **Assigned Member**: Aditya
* **Estimated Time**: 4 hours
* **Label**: Planning
* **Due Date**: 2026-07-06

### Card 02: Trello Card Generation & Task Breakdown
* **Description**: Create and outline 50+ detailed tasks for all team members.
* **Checklist**:
  - [x] Break down features into granular tasks
  - [x] Assign estimates, roles, and due dates
  - [x] Save board state to docs/trello_board.md
* **Priority**: High
* **Assigned Member**: Aditya
* **Estimated Time**: 6 hours
* **Label**: Planning
* **Due Date**: 2026-07-06

### Card 03: Environment Setup & Requirements Identification
* **Description**: Identify all external libraries (Flask, Pandas, NumPy, Scikit-learn, etc.) and create initial requirements list.
* **Checklist**:
  - [x] Research package dependencies
  - [x] Draft requirements.txt file
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 2 hours
* **Label**: Architecture
* **Due Date**: 2026-07-07

### Card 04: Define Folder Directory Structure
* **Description**: Map out all folders (app, models, services, static, templates, tests, data, docs) to follow a professional academic layout.
* **Checklist**:
  - [x] Confirm workspace structure
  - [x] Document folders in README
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 1.5 hours
* **Label**: Architecture
* **Due Date**: 2026-07-07

### Card 05: Establish Team Git Branching Policies
* **Description**: Design git merge guidelines and branching protocols.
* **Checklist**:
  - [x] Define naming conventions for branches
  - [x] Document PR checklist for Aditya
* **Priority**: Medium
* **Assigned Member**: Aditya
* **Estimated Time**: 2 hours
* **Label**: DevOps
* **Due Date**: 2026-07-06

---

## Column: To Do

### Card 06: Data Design - Teams Dataset Scheme
* **Description**: Establish structure for `teams.csv` to ensure all necessary fields are captured.
* **Checklist**:
  - [ ] Define columns: TeamID, Name, Founded, City, Stadium, Capacity, Manager, Mascot
  - [ ] Finalize CSV column order
* **Priority**: High
* **Assigned Member**: Jesis
* **Estimated Time**: 2 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-08

### Card 07: Data Design - Players Dataset Scheme
* **Description**: Establish attributes for `players.csv` containing performance statistics.
* **Checklist**:
  - [ ] Define columns: PlayerID, Name, Age, Position, Club, Nationality, Goals, Assists, Yellow Cards, Red Cards, Matches Played, Minutes Played, Rating
  - [ ] Confirm position values (Forward, Midfielder, Defender, Goalkeeper)
* **Priority**: High
* **Assigned Member**: Jesis
* **Estimated Time**: 3 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-08

### Card 08: Data Design - Matches Dataset Scheme
* **Description**: Outline attributes for matches in the Nepal context.
* **Checklist**:
  - [ ] Define columns: MatchID, Home Team, Away Team, Date, Venue, Goals, Possession, Shots, Shots on Target, Corners, Yellow Cards, Red Cards, Winner
  - [ ] Add columns for HomeGoals, AwayGoals to assist cleaning
* **Priority**: High
* **Assigned Member**: Jesis
* **Estimated Time**: 3 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-08

### Card 09: Data Design - Standings Dataset Scheme
* **Description**: Design schema for `standings.csv` to capture points and league metrics.
* **Checklist**:
  - [ ] Define columns: Position, Team, Played, Won, Drawn, Lost, GF, GA, GD, Points
* **Priority**: Medium
* **Assigned Member**: Jesis
* **Estimated Time**: 2 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-09

### Card 10: Create Teams Raw Data (10 Nepal Clubs)
* **Description**: Compile realistic information for 10 top Nepal clubs.
* **Checklist**:
  - [ ] Create data entries for Machhindra FC, Church Boys United, Three Star Club, Tribhuvan Army FC, Nepal Police Club, APF Club, Jawalakhel Youth Club, Sankata Club, Friends Club, Himalayan Sherpa Club.
* **Priority**: High
* **Assigned Member**: Jesis
* **Estimated Time**: 3 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-09

### Card 11: Create Players Raw Data (50+ records)
* **Description**: Compile a list of at least 50 realistic players distributed among the 10 clubs.
* **Checklist**:
  - [ ] Generate 50+ player rows with realistic stats
  - [ ] Match positions and stats to club quality
* **Priority**: High
* **Assigned Member**: Jesis
* **Estimated Time**: 4 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-09

### Card 12: Create Matches Raw Data (30+ records)
* **Description**: Write detailed records of matches played in Nepal venues.
* **Checklist**:
  - [ ] Generate 30+ matches with goals, cards, and shots
  - [ ] Ensure date values are in correct format
* **Priority**: High
* **Assigned Member**: Jesis
* **Estimated Time**: 4 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-09

### Card 13: Create Initial Standings Dataset
* **Description**: Compute initial standings data matching match history raw output.
* **Checklist**:
  - [ ] Construct points, GD, GF, GA based on the 30 matches
* **Priority**: Medium
* **Assigned Member**: Jesis
* **Estimated Time**: 2 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-09

### Card 14: Implement Data Loader Service (`loader.py`)
* **Description**: Program loader module to read raw CSV files into Pandas DataFrames.
* **Checklist**:
  - [ ] Handle relative file pathways
  - [ ] Implement error handling for missing files
* **Priority**: High
* **Assigned Member**: Jesis
* **Estimated Time**: 3 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-10

### Card 15: Implement Preprocessing Service (`preprocessing.py`)
* **Description**: Develop cleaning script to remove duplicate entries, format date strings, fill missing data.
* **Checklist**:
  - [ ] Deduplicate dataframes
  - [ ] Handle NaN values for cards and ratings
* **Priority**: High
* **Assigned Member**: Jesis
* **Estimated Time**: 4 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-10

### Card 16: Implement General Stats Service (`statistics.py`)
* **Description**: Code calculations for overall goals, assists, clean sheets, and card counts.
* **Checklist**:
  - [ ] Calculate total and averages
  - [ ] Group values by club
* **Priority**: High
* **Assigned Member**: Jesis
* **Estimated Time**: 4 hours
* **Label**: Data-Engineering
* **Due Date**: 2026-07-10

### Card 17: Review Jesis Data Engineering Deliverables
* **Description**: Review code in `loader.py`, `preprocessing.py`, and `statistics.py` for mathematical accuracy.
* **Checklist**:
  - [ ] Verify CSV columns correspond to expectations
  - [ ] Test dataframe cleaning outputs
* **Priority**: Critical
* **Assigned Member**: Sahid
* **Estimated Time**: 3 hours
* **Label**: Testing
* **Due Date**: 2026-07-11

### Card 18: Design Team Model Class (`team.py`)
* **Description**: Write the Team model structure in OOP form.
* **Checklist**:
  - [ ] Model team initialization variables
  - [ ] Add summary representation helper
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 2 hours
* **Label**: Architecture
* **Due Date**: 2026-07-12

### Card 19: Design Player Model Class (`player.py`)
* **Description**: Write the Player model mapping CSV rows to objects.
* **Checklist**:
  - [ ] Model player properties
  - [ ] Implement utility methods (e.g., scoring rate per minute)
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 2 hours
* **Label**: Architecture
* **Due Date**: 2026-07-12

### Card 20: Design Match Model Class (`match.py`)
* **Description**: Construct Match class representation.
* **Checklist**:
  - [ ] Model match events and metrics
  - [ ] Add win/draw checking functions
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 2 hours
* **Label**: Architecture
* **Due Date**: 2026-07-12

### Card 21: Implement Team Analysis Service (`team_analysis.py`)
* **Description**: Perform deeper analytics on home wins, away wins, goals scored, and concession trends.
* **Checklist**:
  - [ ] Compute head-to-head match history between two clubs
  - [ ] Calculate home vs away win conversion ratios
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 4 hours
* **Label**: Backend-Dev
* **Due Date**: 2026-07-13

### Card 22: Implement Player Analysis Service (`player_analysis.py`)
* **Description**: Create player performance indexes, comparison matrices, and efficiency ratings.
* **Checklist**:
  - [ ] Rank players by goals + assists index
  - [ ] Set up player card compare values
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 4 hours
* **Label**: Backend-Dev
* **Due Date**: 2026-07-13

### Card 23: Implement Match Analysis Service (`match_analysis.py`)
* **Description**: Synthesize match goals, possession percentages, and referee warning counts.
* **Checklist**:
  - [ ] Group matches by date and venue
  - [ ] Calculate average goals per match overall
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 3 hours
* **Label**: Backend-Dev
* **Due Date**: 2026-07-14

### Card 24: Implement ML Outcome Prediction Service (`predictions.py`)
* **Description**: Code a classifier to predict home wins, away wins, or draws based on team ratings.
* **Checklist**:
  - [ ] Preprocess matches into training vectors (HomeTeamRating, AwayTeamRating, etc.)
  - [ ] Train a Scikit-Learn model (e.g. Random Forest / Logistic Regression)
  - [ ] Expose predict function returning probabilities
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 6 hours
* **Label**: Backend-Dev
* **Due Date**: 2026-07-15

### Card 25: Implement Analytical Charts Service (`visualization.py`)
* **Description**: Write helper functions to plot charts with Matplotlib/Seaborn and save to static assets.
* **Checklist**:
  - [ ] Create top goals bar chart
  - [ ] Draw possession vs wins scatter plot
  - [ ] Generate goals distribution histogram
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 5 hours
* **Label**: Backend-Dev
* **Due Date**: 2026-07-14

### Card 26: Implement Dashboard Metric Hub (`analytics.py`)
* **Description**: Synthesize high level figures (total clubs, active players, goals/match average, top team) for the main view.
* **Checklist**:
  - [ ] Calculate total stats counts
  - [ ] Cache dashboard parameters
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 3 hours
* **Label**: Backend-Dev
* **Due Date**: 2026-07-13

### Card 27: Implement Common Utilities (`utils.py`)
* **Description**: Compile helper functions for styling, currency/formatting, and dictionary parsing.
* **Checklist**:
  - [ ] Create positional abbreviation converters
  - [ ] Implement rating color helper
* **Priority**: Low
* **Assigned Member**: Bishal
* **Estimated Time**: 2 hours
* **Label**: Backend-Dev
* **Due Date**: 2026-07-12

---

## Column: Doing

### Card 28: Flask App Factory Configuration (`__init__.py`)
* **Description**: Initialize Flask app, define application configuration, and register blueprint routes.
* **Checklist**:
  - [ ] Write App Factory setup
  - [ ] Add static/template folders pointing
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 3 hours
* **Label**: Backend-Dev
* **Due Date**: 2026-07-16

### Card 29: Flask Routes Controller Development (`routes.py`)
* **Description**: Write controller action mappings linking requests to services and views.
* **Checklist**:
  - [ ] Define routes for all 10 templates
  - [ ] Implement search query arguments parser
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 6 hours
* **Label**: Backend-Dev
* **Due Date**: 2026-07-17

### Card 30: Design Core CSS Theme (`main.css`)
* **Description**: Set up the project's styling using responsive dark gradients, custom typography, and hover animations.
* **Checklist**:
  - [ ] Choose sleek dark-theme palettes with primary green/blue accents
  - [ ] Write responsive media queries
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 4 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-18

### Card 31: Build Base Layout Template (`base.html`)
* **Description**: Construct generic base file containing navbar, responsive sidebar, standard scripts, and footer.
* **Checklist**:
  - [ ] Integrate Bootstrap 5 CDN and custom fonts
  - [ ] Build responsive sidebar toggling mechanism
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 4 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-18

### Card 32: Build Dashboard Home View (`index.html`)
* **Description**: Put together summary cards, recent fixtures carousel, and team points overview.
* **Checklist**:
  - [ ] Create counters for players, matches, and clubs
  - [ ] Embed league standings summary
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 4 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-19

### Card 33: Build Clubs Directory View (`teams.html`)
* **Description**: Showcase club rosters and profiles. Include side-by-side team comparisons.
* **Checklist**:
  - [ ] Display club grid cards
  - [ ] Design team comparison selectors
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 5 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-20

### Card 34: Build Players Grid View (`players.html`)
* **Description**: Design a search-and-filter players index with goals, ratings, and positional filters.
* **Checklist**:
  - [ ] Add player cards layout
  - [ ] Build dynamic player selection comparison form
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 5 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-20

---

## Column: Code Review

### Card 35: Build Matches History View (`matches.html`)
* **Description**: Present a list of played matches and fixtures with search fields for home/away teams.
* **Checklist**:
  - [ ] Render timeline-style matches schedule
  - [ ] Highlight winners and goal scorers
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 4 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-21

### Card 36: Build League Statistics Page (`statistics.html`)
* **Description**: List league tables, top scorers (Golden Boot), assists, and card aggregations.
* **Checklist**:
  - [ ] Construct sorted scorers data table
  - [ ] Render card offenders ranking
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 4 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-21

### Card 37: Build Custom Analytics Page (`analytics.html`)
* **Description**: Provide in-depth statistical breakdowns, such as home ground advantage analysis.
* **Checklist**:
  - [ ] Render percentage breakdown charts
  - [ ] Present stadium capacity versus team performance correlations
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 4 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-22

### Card 38: Build Visualizations Dashboard (`visualization.html`)
* **Description**: Embed static Matplotlib/Seaborn charts and set up interactive Chart.js elements.
* **Checklist**:
  - [ ] Create chart placeholders
  - [ ] Integrate Chart.js canvas elements for client-side loading
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 5 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-22

### Card 39: Build Match Prediction Simulator (`prediction.html`)
* **Description**: Interface allowing users to select two teams and see win probability predictions.
* **Checklist**:
  - [ ] Create home team and away team dropdown select menus
  - [ ] Embed prediction result graphs/bars
* **Priority**: High
* **Assigned Member**: Bishal
* **Estimated Time**: 5 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-23

### Card 40: Build Project Information Page (`about.html`)
* **Description**: Detail project scope, developer team, and Trello board overview.
* **Checklist**:
  - [ ] Write bios for Jesis, Sahid, Bishal, Aditya
  - [ ] Add university module guidelines reference
* **Priority**: Low
* **Assigned Member**: Bishal
* **Estimated Time**: 3 hours
* **Label**: Frontend-Dev
* **Due Date**: 2026-07-24

### Card 41: Main Application Runner Configuration (`run.py`)
* **Description**: Create entry-point run script configuring host and port parameters.
* **Checklist**:
  - [ ] Write startup script importing app factory
  - [ ] Set up debug conditional arguments
* **Priority**: Medium
* **Assigned Member**: Bishal
* **Estimated Time**: 1 hour
* **Label**: Backend-Dev
* **Due Date**: 2026-07-16

### Card 42: Validate Backend Prediction Algorithm
* **Description**: Rigorously verify predicted probabilities output from the ML models.
* **Checklist**:
  - [ ] Test edge cases (team vs itself)
  - [ ] Check prediction output formats match expected JSON objects
* **Priority**: Critical
* **Assigned Member**: Sahid
* **Estimated Time**: 4 hours
* **Label**: Testing
* **Due Date**: 2026-07-24

### Card 43: Validate Frontend Templates responsiveness
* **Description**: Review Bootstrap grid styling and check elements layout on mobile screens.
* **Checklist**:
  - [ ] Inspect pages at 375px width (mobile)
  - [ ] Fix overlapping sidebar text issues
* **Priority**: Medium
* **Assigned Member**: Sahid
* **Estimated Time**: 3 hours
* **Label**: Testing
* **Due Date**: 2026-07-25

---

## Column: Testing

### Card 44: Write CSV Loader Unit Tests (`test_loader.py`)
* **Description**: Create test assertions verifying correct file parsing.
* **Checklist**:
  - [ ] Test missing file raising FileNotFoundError
  - [ ] Verify dataset shape match
* **Priority**: High
* **Assigned Member**: Sahid
* **Estimated Time**: 3 hours
* **Label**: Testing
* **Due Date**: 2026-07-26

### Card 45: Write Preprocessing Unit Tests (`test_preprocessing.py`)
* **Description**: Ensure cleaning pipelines properly drop duplicate rows.
* **Checklist**:
  - [ ] Input synthetic dirty dataframe
  - [ ] Assert duplicates are removed
* **Priority**: High
* **Assigned Member**: Sahid
* **Estimated Time**: 3 hours
* **Label**: Testing
* **Due Date**: 2026-07-26

### Card 46: Write League Statistics Unit Tests (`test_statistics.py`)
* **Description**: Verify aggregated calculations like points and goals.
* **Checklist**:
  - [ ] Test sum statistics formulas
  - [ ] Assert win % and points math matches standings rules
* **Priority**: High
* **Assigned Member**: Sahid
* **Estimated Time**: 3 hours
* **Label**: Testing
* **Due Date**: 2026-07-26

### Card 47: Write Visualization Unit Tests (`test_visualization.py`)
* **Description**: Ensure matplotlib files are written to the correct folder.
* **Checklist**:
  - [ ] Test chart creation methods
  - [ ] Assert png files exist after script runs
* **Priority**: Medium
* **Assigned Member**: Sahid
* **Estimated Time**: 2 hours
* **Label**: Testing
* **Due Date**: 2026-07-27

### Card 48: Write Prediction Model Unit Tests (`test_prediction.py`)
* **Description**: Check ML model output probability ranges.
* **Checklist**:
  - [ ] Verify return prediction range between [0, 1]
  - [ ] Assert winner output matches logic boundaries
* **Priority**: High
* **Assigned Member**: Sahid
* **Estimated Time**: 3 hours
* **Label**: Testing
* **Due Date**: 2026-07-27

### Card 49: Write Routing Controller Unit Tests (`test_routes.py`)
* **Description**: Set up Flask test client to verify GET requests.
* **Checklist**:
  - [ ] Assert index route returns status code 200
  - [ ] Confirm prediction results JSON endpoint response code
* **Priority**: High
* **Assigned Member**: Sahid
* **Estimated Time**: 4 hours
* **Label**: Testing
* **Due Date**: 2026-07-27

---

## Column: Done

### Card 50: Create Professional README File
* **Description**: Compose extensive root level documentation outlining project setup.
* **Checklist**:
  - [ ] Describe installation procedures
  - [ ] Create directory structure graph
  - [ ] Add guidelines on how to run tests
* **Priority**: High
* **Assigned Member**: Aditya
* **Estimated Time**: 5 hours
* **Label**: Documentation
* **Due Date**: 2026-07-28

### Card 51: Compile User Manual (`user_manual.md`)
* **Description**: Draft step-by-step user interactions guidebook.
* **Checklist**:
  - [ ] Document prediction simulation steps
  - [ ] Document team comparisons flow
* **Priority**: Medium
* **Assigned Member**: Aditya
* **Estimated Time**: 4 hours
* **Label**: Documentation
* **Due Date**: 2026-07-28

### Card 52: Generate API Specifications (`api_docs.md`)
* **Description**: Document route endpoints and JSON payload parameters.
* **Checklist**:
  - [ ] Document Flask routes
  - [ ] Detail prediction inputs format
* **Priority**: Medium
* **Assigned Member**: Aditya
* **Estimated Time**: 3 hours
* **Label**: Documentation
* **Due Date**: 2026-07-28

### Card 53: Write Final Project Report (`final_report.md`)
* **Description**: Compile university standard final software engineering project report.
* **Checklist**:
  - [ ] Outline architecture, models, and ML predictions
  - [ ] Detail verification and validation outcomes
* **Priority**: High
* **Assigned Member**: Aditya
* **Estimated Time**: 6 hours
* **Label**: Documentation
* **Due Date**: 2026-07-29

### Card 54: Create & Review Pull Requests
* **Description**: Act as lead developer to create and review pull requests from feature branches into main.
* **Checklist**:
  - [ ] Create PRs for Jesis, Bishal, and Sahid branches
  - [ ] Double-check and verify code changes
* **Priority**: Critical
* **Assigned Member**: Aditya
* **Estimated Time**: 4 hours
* **Label**: DevOps
* **Due Date**: 2026-07-30

### Card 55: Merge Branches and Run Live Integration Testing
* **Description**: Resolve any conflicts, perform final merge into main, and test.
* **Checklist**:
  - [ ] Perform git merge
  - [ ] Execute test suite and verify no failing checks
* **Priority**: Critical
* **Assigned Member**: Aditya
* **Estimated Time**: 4 hours
* **Label**: DevOps
* **Due Date**: 2026-07-30
