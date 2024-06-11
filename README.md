# ff-league-app

### Directory

discord-yahoo-fantasy-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── fantasy.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── yahoo_api.py
│   └── config/
│       ├── __init__.py
│       ├── settings.py
├── data/
│   ├── .gitignore
│   └── example_data_file.json
├── requirements.txt
├── .env
├── .gitignore
└── README.md

### Explanation

1. `bot/`: The main directory for the bot code
- `__init__.py`: Makes the bot directory a package.
- `main.py`: The entry point for the bot. It will contain the code to start the bot and set up event handlers.
- `commands/`: A subdirectory for bot commands.
    - `__init__.py`: Makes the `commands` directory a package. 
    - `fantasy.py`: Contains the commands related to Yahoo Fantasy API.
- `utils/`: A subdirectory for utility functions and modules.
    - `__init__.py` Makes the `utils` directory a package.
    - `fantasy_api.py`: Contains functions to interact with the Yahoo Fantasy API using `yfpy`.
- `config/`: A subdirectory for configuration files.
    - `__init__.py`: Makes the `config` directory a package.
    - `settings.py`: Contains bot settings and configurations.
- `data/`: A directory to store data files.
    - `.gitignore`: Ensures that sensitive or large data files are not tracked by Git.
- `requirements.txt`: Lists the Python dependencies for the bot. 
- `.env`: Contains environment variables such as API keys and tokens (not to be tracked by Git for security reasons).
- `README.md`: You're looking at it!
