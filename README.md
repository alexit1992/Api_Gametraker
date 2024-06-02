# DiscordAPIgame
# Discord Game Server Info Bot

This is a Discord bot that fetches and displays information about game servers. It allows users to register and check the status of game servers directly from a Discord server.

## Features
- Fetch and display information about game servers.
- Register new users with email, birth date, and password.
- Save and update game server information in a MySQL database.

## Installation

### Prerequisites
- Python 3.8 or later
- pip (Python package installer)
- MySQL server
- Discord bot token
- API token for fetching game data

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/alexit1992/Api_Gametraker-.git
    cd BreadcrumbsApi_Gametraker-
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory of the project.
    - Add the following environment variables to the `.env` file:
    ```ini
    DISCORD_TOKEN=your_discord_bot_token
    API_TOKEN=your_api_token
    API_TOKEN_TYPE=your_api_token_type
    API_TOKEN_EMAIL=your_api_token_email
    DB_HOST=your_database_host
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_NAME=your_database_name
    ```

5. **Set up the MySQL database**:
    - Create a new MySQL database.
    - Create the required tables (e.g., `servers`) using the following SQL schema:
    ```sql
    CREATE TABLE servers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ip VARCHAR(255) NOT NULL,
        name VARCHAR(255),
        map VARCHAR(255),
        players INT
    );
    ```

## Usage

### Running the Bot

To start the bot, run the following command:
```bash
python bot.py
Commands
/server ip:port: Fetches and displays information about the specified game server.
/register <email> <birth_date> <password>: Registers a new user with the provided email, birth date, and password.
Example
plaintext
Code kopieren
User: /server 12.34.56.78:27015
Bot: 
Informații despre Server
Nume: My Game Server
Hartă: de_dust2
Protejat cu parolă: Nu

Jucători online:
markdown
Code kopieren
Nume                 Score
------------------------------
Player1              10
Player2              15
Troubleshooting
If you encounter any issues, please check the following:

Ensure that all environment variables are correctly set in the .env file.
Verify that the MySQL database is running and accessible.
Check that the API token is valid and has the necessary permissions.
Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License. See the LICENSE file for details.

javascript
Code kopieren

Replace `your_discord_bot_token`, `your_api_token`, `your_api_token_type`, `your_api_token_email`, `your_database_host`, `your_database_user`, `your_database_password`, and `your_database_name` with your actual credentials and configuration details.

This README file provides a comprehensive overview of your bot, including it
