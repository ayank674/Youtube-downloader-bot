# Youtube-downloader-bot

A Telegram bot that enables users to download YouTube videos by sending links, with features for user and admin management.

## Features

- **Video Downloads**: Users can download YouTube videos by replying to a link with the `/download` command.
- **User Management**: Admins can add users, and the owner can add admins, list users or admins, and remove users or admins.
- **Data Persistence**: Utilizes a PostgreSQL database to store user and admin data.
- **Easy Deployment**: Deployable on Render with straightforward environment variable configuration.

## Requirements

- A Telegram account and a bot created via @BotFather.
- A Render account for deployment ([Render](https://render.com)).
- A PostgreSQL database, set up on Render.

## Installation

1. **Create a Telegram Bot**:
   - Open Telegram and interact with @BotFather to create a new bot.
   - Save the `BOT_TOKEN` provided by @BotFather.

2. **Obtain Telegram API Credentials**:
   - Visit [my.telegram.org](https://my.telegram.org/apps) and log in with your Telegram account.
   - Create a new app to obtain the `API_ID` and `API_HASH`.

3. **Deploy on Render**:
   - Sign up for a Render account at [render.com](https://render.com).
   - Navigate to the [New Web Service page](https://dashboard.render.com/select-repo?type=web).
   - Paste the repository URL: [https://github.com/ayank674/Youtube-downloader-bot](https://github.com/ayank674/Youtube-downloader-bot).
   - Assign a name to your web service.
   - In the "Advanced" settings, add the following environment variables:
     - `OWNER`: Your Telegram user ID (obtain from @userinfobot).
     - `SESSION_NAME`: A name for the bot’s session (e.g., "youtube_downloader").
     - `API_ID`: From step 2.
     - `API_HASH`: From step 2.
     - `BOT_TOKEN`: From step 1.
     - `CRASH_MESSAGE`: A custom error message (e.g., "An error occurred. Please try again later.").
   - Create a PostgreSQL database on Render and link it to your web service. Render will automatically set the `DATABASE_URL` environment variable.
   - Click "Create Web Service" to deploy the bot.

## Usage

Once the bot is deployed, interact with it on Telegram using the following commands:

- **General Commands**:
  - `/start`: Check if the bot is active.
  - `/download`: Reply to a YouTube link with this command to initiate the download process.

- **Admin Commands**:
  - `/add_user`: Reply to a user’s message with their ID to add them as a user.

- **Owner Commands**:
  - `/add_admin`: Add a user as an admin.
  - `/display_users`: List all registered users.
  - `/display_admins`: List all admins.
  - `/remove_user`: Remove a user or admin.

## Configuration

The bot requires the following environment variables for operation:

| Variable        | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `OWNER`         | Your Telegram user ID, obtainable via @userinfobot.                         |
| `SESSION_NAME`  | A name for the bot’s session (e.g., "youtube_downloader").                  |
| `API_ID`        | Telegram API ID from my.telegram.org.                                       |
| `API_HASH`      | Telegram API hash from my.telegram.org.                                     |
| `BOT_TOKEN`     | The bot’s token provided by @BotFather.                                     |
| `CRASH_MESSAGE` | A custom message displayed when errors occur.                               |
| `DATABASE_URL`  | URL of the PostgreSQL database, automatically set by Render.                |

## Troubleshooting

- **Bot Not Responding**: Check Render logs for errors, ensuring all environment variables are correctly set.
- **Database Issues**: Verify that the PostgreSQL database is linked and accessible via the `DATABASE_URL`.
- **Command Errors**: Ensure you have the correct permissions (user, admin, or owner) for specific commands.

## Dependencies

The bot relies on the following Python packages, as specified in `requirements.txt`:

| Package        | Version  | Purpose                              |
|----------------|----------|--------------------------------------|
| cffi           | 1.15.1   | Foreign function interface           |
| psycopg        | 3.1.19   | PostgreSQL database adapter          |
| pyaes          | 1.6.1    | AES encryption                       |
| pycparser      | 2.21     | C parser for cffi                    |
| Pyrogram       | 2.0.106  | Telegram bot framework               |
| PySocks        | 1.7.1    | SOCKS proxy support                  |
| pytube         | 15.0.0   | YouTube video downloading            |
| TgCrypto       | 1.2.5    | Cryptography for Pyrogram            |
| Flask          | 2.3.2    | Web framework for health checks      |
| gunicorn       | 21.2.0   | WSGI server for Flask                |
| aiohttp        | 3.8.5    | Asynchronous HTTP client/server      |
| pytubefix      | 8.12.1   | Enhanced YouTube downloading         |

These dependencies are automatically installed when deploying on Render.

## License

The license for this project is not specified in the provided documentation. Check the repository for a LICENSE file or contact the author for clarification.
