# the squirrel from VandyHacks
VandyHacks VII Discord Bot

## Developer Setup

the squirrel from VandyHacks requires Python 3.6+ (we use f-strings lol).

### Installation

Clone the repo by 
`git clone https://github.com/VandyHacks/the-squirrel-from-VandyHacks.git` or use ssh.

`cd` into the repo and do `pip install -r requirements.txt` (or pip3) to install dependencies.

### Secrets
Create a file named `.env` in the repo and add your discord token to it like `DISCORD=your_token_here`.
This is what links the application to your bot profile.

### Database
This part is only required if you're working on the quests command.

For quests, there is a PostgreSQL DB to store the hacker's current quest level.
Get Postgres if you don't have it already and make a database called `vh`.

Add your Postgres user and password to the `.env` file like `DB_USER=username` and `DB_PASSWD=password`.

### Run

That's it ez pz you're done.

Run the bot using 

```commandline
python3 bot.py
```
or `python bot.py` if you're on Windows or using a virtualenv or something.

![Vandy Gold Heart](https://cdn.discordapp.com/attachments/424321814702063647/750174332982001746/gold_heart.png)
