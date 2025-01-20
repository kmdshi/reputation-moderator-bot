## Reputation Bot for Telegram

The bot allows moderators to increase or decrease participants' reputation, track reputation changes, and block spam or inappropriate messages. The bot is still under development and may be extended with new features.

### Bot Features:
- **Manage user reputation:** Moderators can increase or decrease a user's reputation using commands.
- **View reputation:** Users can request to see the current reputation of other participants.
- **Filter spam or other inappropriate messages:** The bot tracks changes in user reputation with the ability to view changes over a specific period.
- **Manage users:** Ban, mute, etc.

### Commands:
- `/mute(unmute_user) @username` — Mute or unmute a user.
- `!report` — Report an issue or inappropriate content.
- `$help` — Get a list of available commands.
- `%about` — Information about the bot.

### Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/reputation-bot.git
2.  Install dependencies:
```pip install -r requirements.txt```\
3. Configure the bot token in the config.py file.\
4.Create a .env file:
```
TOKEN=your-telegram-bot-token
db_path=your-db-path
keywords_words=your-keyword-for-filter
```
5. Start the bot:
```python main.py```
### License:
This project is licensed under the MIT License.
