import os

import sqlalchemy
from databases import Database
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

meta = sqlalchemy.MetaData()

# more like questers but that word seems weird
Hacker = sqlalchemy.Table(
    "hackers",
    meta,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.BigInteger, unique=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(length=40), nullable=False),  # just for convenience
    sqlalchemy.Column("level", sqlalchemy.BigInteger, nullable=False, server_default="0"),
)

# squirrel pat counter
Pats = sqlalchemy.Table(
    "pats",
    meta,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("pat", sqlalchemy.Integer, nullable=False, server_default="0"),
)

ENGINE = None

"""
 you should manually initialize the db for first run since it's a sync call
 it will create the table locally
 >>> from database import meta, DATABASE_URL
 >>> import sqlalchemy
 >>> meta.create_all(sqlalchemy.create_engine(DATABASE_URL))
"""


async def prepare_engine():
    global ENGINE  # reuse connection
    if ENGINE is None:
        ENGINE = Database(DATABASE_URL)
        await ENGINE.connect()
    return ENGINE


# add db entry for hackers
async def make_hacker_profile(hackers):
    engine = await prepare_engine()
    create_query_values = []

    for hacker in hackers:
        if hacker.bot:
            continue
        exists_query = Hacker.select().where(Hacker.c.user_id == hacker.id)
        res = await engine.fetch_one(query=exists_query)

        if not res:  # user doesn't exist
            create_query_values.append({"user_id": hacker.id, "name": str(hacker)})
            print(f"Creating profile for {hacker.name}")

    if create_query_values:
        create_query = Hacker.insert()
        await engine.execute_many(query=create_query, values=create_query_values)


async def get_quest_level(hacker):
    # hacker will be a discord.User
    engine = await prepare_engine()
    select_query = Hacker.select().where(Hacker.c.user_id == hacker.id)
    res = await engine.fetch_one(query=select_query)
    return res[Hacker.c.level]


async def update_quest_level(hacker):
    engine = await prepare_engine()
    # increment level by one
    update_query = Hacker.update().where(Hacker.c.user_id == hacker.id).values(level=Hacker.c.level + 1)
    await engine.execute(update_query)


async def init_pats():
    # add pat row if doesn't exist already
    engine = await prepare_engine()
    exists_query = Pats.select().where(Pats.c.id == 0)
    res = await engine.fetch_one(query=exists_query)

    if not res:  # user doesn't exist
        create_query = Pats.insert()
        print("initializing pat counter")
        await engine.execute(query=create_query, values={"id": 0, "pat": 0})


async def update_pat_counter():
    engine = await prepare_engine()
    # increment pats by one, and return new val
    update_query = Pats.update().where(Pats.c.id == 0).values(pat=Pats.c.pat + 1).returning(Pats.c.pat)
    count = await engine.execute(update_query)
    print(f"increased pat count to {count}")
    return count
