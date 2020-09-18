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
    sqlalchemy.Column("name", sqlalchemya.String(length=40), nullable=False),  # just for convenience
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
