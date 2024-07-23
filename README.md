# ff-league-app

This project is a Discord bot that pulls data from the Yahoo Fantasy API using the `yfpy` open source wrapper.

Currently, the Bot, "Marcy," pocesses the following functionality:

1. Retreives standings.
2. Retreives matchups.
3. Pulls NFL statistics.
4. Calculates power rankings.

I am currently working on a script that will pull historical data from all 12 of our seasons and store them in a relational database. From there,
I intend on implemented the following features:

1. Playoff offs calculautes using Monte Carlo simulations.
2. Leveraging a modern LLM to generate commentary along with the weekly power rankings.
3. A dedicated website to showcase historical statitics and in-season analytics.