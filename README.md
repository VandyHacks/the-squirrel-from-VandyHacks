# the squirrel from VandyHacks

The VandyHacks VII Discord Bot.

If you’re looking to use the squirrel from VandyHacks for your hackathon (thanks <3 if you’re the ones already doing it!), take a look at the Developer Setup and Architecture sections below for an overview. 

## Developer Setup

the squirrel from VandyHacks requires Python 3.8+ (we use the walrus operator lol).

### Installation

Clone the repo by 
`git clone https://github.com/VandyHacks/the-squirrel-from-VandyHacks.git` or use ssh.

`cd` into the repo and do `pip install -r requirements.txt` (or pip3) to install dependencies.

### Secrets

Create a file named `.env` in the repo and add your discord token to it like `DISCORD=your_token_here`.
This is what links the application to your bot profile.

### Database
This part is only required if you're working on the quest or pat command.

For quests, there is a PostgreSQL DB to store the hacker's current quest level and the number of 
times the squirrel has been pet.

Get Postgres if you don't have it already and make a database called `vh`.

Add your Postgres user and password to the `.env` file like `DB_USER=username` and `DB_PASSWD=password`.

Look into `database.py` on how to create tables for first run.

### Run

That's it ez pz you're done.

Run the bot using 

```commandline
python3 bot.py
```
or `python bot.py` if you're on Windows or using a virtualenv or something.

## Architecture

Here is all you need to know about how the bot is set up and the functionality the squirrel from VandyHacks offers.

```
├── bot.py
├── cogs
│   ├── __init__.py
│   ├── info.py
│   ├── quest.py
│   └── times.py
├── database.py
└── utils.py
```

Let me run you down the structure, `bot.py` houses the code where the bot is initialized and general commands like help and event listeners are defined. (also an easter egg but shhh)

`database.py` is pretty much self-explanatory, it has the postgres engine as well as functions to create and update the hacker quest levels and squirrel pat counter. 

Cogs basically mean classes which contain related commands so they’re not all bunched in one file and it is easier to read and maintain.

The Info cog (`info.py`) has commands that display info about your hackathon and the bot itself, such as important links, the hacker guide, bot deployment info and github url.

The Times cog (`times.py`) is the file that contain the very useful `vh when` and `vh schedule` commands. These commands display the event schedule as an interactive paginated embed with the time zone agnostic duration until the event.

<img src="https://i.imgur.com/XFyPN2o.png" alt="vh schedule" style="zoom: 67%;" />

This is very useful, especially for online hackathons since it saves those pesky tz conversions that you would otherwise be doing. 

`utils.py` just contains a function that takes a list of embeds and adds the interactive pagination functionality to it, it is used in the schedule command.

The Quest cog (`quest.py`) houses everything that goes into `vh quest`, the ctf style cryptic treasure hunt we had in VH VII. You can look at the controller function along with the challenges/flags in there, honestly would be pretty cool if someone went ahead and used it.

That is it, we hope you have fun and let us know if you have any questions!

![Vandy Gold Heart](https://cdn.discordapp.com/attachments/424321814702063647/750174332982001746/gold_heart.png)