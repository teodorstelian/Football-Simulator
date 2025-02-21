# Football Simulator
====================================

A **Python-based football simulation program** that lets you explore different outcomes for professional football leagues, cups, and European tournaments. Perfect for football enthusiasts who love to simulate, analyze, or create alternative football histories!

---

## Requirements
- **Python 3.9 or higher**

---

## Features
### ✅ General Features:
- Simulate games based on team skills, league standings, and competition rules.
- Supports simulation of **29 top European leagues**

### ⚽ League Features:
- Simulate full **league seasons** for all supported leagues.
- Includes league-specific rules, standings, and points calculations.

### 🏆 Cup Features:
- Simulate **national football cups** for each of the supported countries.
- National cups include the **top 16 teams** from the respective leagues.

### 🌍 European Competitions:
- Simulate European tournaments in a Knockout style:
  - **UEFA Champions League (UCL)**.
  - **UEFA Europa League (UEL)**.
  - **UEFA Europa Conference League (UECL)**.
- Track European appearances and wins for each team.

### 📊 Statistics & History:
- Store and retrieve historical data in a relational database.
- Track stats such as:
  - Team records over all simulations.
  - League, national cup, and European tournament winners.
  - Most skilled teams based on skills database.

### 🗓️ Season Simulation:
- Simulate an **entire season**:
  - League.
  - National Cup.
  - All 3 European tournaments (UCL, UEL, UECL).

---

## Upcoming Features
- **Expanded database** with more leagues and teams.
- Larger national cups with more participants.
- Full-scale European tournaments with group stages and qualifications.
- Enhanced statistics tracking:
  - In-depth analytics at team, league, and competition levels.
- Option to export results to various formats (CSV, JSON, etc.).

---

## Usage Instructions

Run the main.py.

You will be presented with the following menu options:

### Main Menu:
| **Option** | **Description**                                                                                  |
|------------|--------------------------------------------------------------------------------------------------|
| **1**      | Simulate an entire season: League → National Cup → All European Cups.                            |
| **2**      | Simulate a specific league season (choose a league via prompt).                                  |
| **3**      | Simulate a specific national cup (choose a country via prompt).                                  |
| **4**      | Play a European cup tournament (**UCL**, **UEL**, or **UECL**).                                  |
| **5**      | View the best-performing teams in a specific league (based on simulation records).               |
| **6**      | Check detailed stats for a specific team (enter team name).                                      |
| **7**      | View the most successful teams in a specific competition (e.g., most league/cup titles).         |
| **8**      | View European competition stats (appearances and wins by teams in UCL/UEL/UECL).                 |
| **9**      | Display the most skilled teams (based on skill metrics defined in the database).                 |
| **q**      | Quit the program.

---

## Example Walkthrough
### Simulating an Entire Season
1. Choose **Option 1**: Simulate an entire season.
2. Specify the number of seasons to simulate.
3. Watch the simulation results as the program:
   - Simulates each country's league and national cup.
   - Plays European competitions (UCL, UEL, UECL).

4. Results will be updated in the database and displayed:
   - League winners, Cup winners, European competition results.

---

## Database Management
The program utilizes a database to store and retrieve historical data. Some of the key data stored includes:
- League results and standings.
- Cup winners by season.
- Historical European appearances and performances (e.g., how often a team reached the UCL final).

---

## Contributing
Contributions are welcome! Feel free to submit pull requests or report issues:
1. Fork the repo.
2. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature-name
   ```
3. Submit your changes with a pull request.
