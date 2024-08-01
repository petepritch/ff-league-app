# ff-league-app

This project is a Discord bot that pulls data from the Yahoo Fantasy API using the `yfpy` open source wrapper.

Currently, the Bot "Marcy" pocesses the following functionality:

1. Retrieves standings.
2. Retrieves matchups status.
3. Pulls NFL statistics.
4. Calculates power rankings.

I am now working on a script that will pull historical data from all 12 of our seasons and store them in a relational database. From there,
I intend on implementing the following features:

1. Playoff odds calculauted using Monte Carlo simulations.
2. Leveraging a modern LLM to generate commentary along with the weekly power rankings.
3. A dedicated website to showcase historical statistics and in-season analytics.

Eventually, I would like to refactor this repo in such a way that other Yahoo Fantasy Football enthusiasts can clone and get this bot up and running for their own leagues with minimal effort. If you stumble upon this page and are interested in contributing to this project, please reach out to me by email - petep <at> umich <dot> edu.