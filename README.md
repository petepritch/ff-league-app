# ff-league-app

This project is a Discord bot that pulls data from the Yahoo Fantasy API using the `yfpy` open source wrapper. Below is the directory structure of the project:

## Directory Structure

- **bot/**: The main directory for the bot code.
  - **__init__.py**: Makes the `bot` directory a package.
  - **main.py**: The entry point for the bot. Contains the code to start the bot and set up event handlers.
  - **commands/**: A subdirectory for bot commands.
    - **__init__.py**: Makes the `commands` directory a package.
    - **fantasy.py**: Contains the commands related to Yahoo Fantasy API.
  - **utils/**: A subdirectory for utility functions and modules.
    - **__init__.py**: Makes the `utils` directory a package.
    - **yahoo_api.py**: Contains functions to interact with the Yahoo Fantasy API using `yfpy`.
  - **config/**: A subdirectory for configuration files.
    - **__init__.py**: Makes the `config` directory a package.
    - **settings.py**: Contains bot settings and configurations.

- **data/**: A directory to store data files (if needed).
  - **.gitignore**: Ensures that sensitive or large data files are not tracked by Git.
  - **example_data_file.json**: An example data file (if needed).

- **requirements.txt**: Lists the Python dependencies for your project.
- **.env**: Contains environment variables such as API keys and tokens (not to be tracked by Git for security reasons).
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **README.md**: Provides an overview of the project and instructions for setup and usage.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/discord-yahoo-fantasy-bot.git
   cd discord-yahoo-fantasy-bot
