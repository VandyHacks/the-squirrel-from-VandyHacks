import os

import sqlalchemy
from databases import Database
from dotenv import load_dotenv
from sqlalchemy.schema import CreateTable

# load environment variables from .env
load_dotenv()

DATABASE_URL = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWD']}@localhost/vh"

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


# add db entry for hacker
async def make_hacker_profile(members_list, self_id):
    engine = await prepare_engine()
    create_query_values = []
    for hacker in members_list:
        if hacker.id == self_id:
            continue
        exists_query = Hacker.select().where(Hacker.c.id == hacker.id)
        res = await engine.fetch_all(query=exists_query)
        if len(res) == 0:
            create_query_values.append({"user_id": hacker.id, "name": str(hacker)})
            logging.debug("Creating profile for member %s.", member.name)
    if len(create_query_values) > 0:
        create_query = Hacker.insert()
        await engine.execute_many(query=create_query, values=create_query_values)


async def get_quest_level(hacker):
    # hacker will be a discord.User
    engine = await prepare_engine()
    print("prepared engine")
    exists_query = Hacker.select().where(Hacker.c.user_id == hacker.id)
    res = await engine.fetch_one(query=exists_query)
    print("fetched query")

    if not res:  # user doesn't exist
        print("user doesn't exist")
        create_query = Hacker.insert()
        create_values = {"user_id": hacker.id, "name": str(hacker)}
        await engine.execute(query=create_query, values=create_values)
        print(f"created user: {create_values}")
        return 0  # since default level is 0

    return res[Hacker.c.level]


