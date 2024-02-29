Football Simulator
====================================

A Django Project where the user can manage a football team.

Requirements
------------
-   Any python environment
-   A browser
 
Features (Legacy - Script Mode)
--------
- Simulate a game between 2 teams based on their skill
- Currently 7 leagues implemented 
(Premier League, Bundesliga, Serie A, Ligue 1, La Liga, Eredivisie and Primeira Liga)
- Simulate a football league
- Simulate a football cup (Top 16 from Country)
- Simulate a small version (16 Teams) of each european cup (UCL, UEL, UECL)
- Simulate a whole season (League + Cup + All 3 European Cups)
- Database that holds all the teams and history of seasons
- Folder with the results of all simulations
- Statistics for each team 

Features (Django App)
-----------
- Database of 30+ players with skills and positions
- Playable teams with first 11 (Chelsea, Liverpool) and many more to be added
- Ability to generate a lineup
- Statistics of top teams, players
- Specific page for every team, player in the database
- Search function
- Ability to start a new game

To be added in the near future
-----------
- Simulation of a game with scores taking in account the skills of players
- Substitutions
- Auto-generate lineup
- Generation of fixtures in a season like
- Addition of more players and teams


Bugs
-----
- When simulating a game, stats update only for the team in right (adds 1 app), nothing for the team on left
