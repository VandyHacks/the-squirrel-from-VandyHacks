import sqlalchemy
from databases import Database
from sqlalchemy.schema import CreateTable

meta = sqlalchemy.MetaData()

# more like questers but that word seems weird
Hacker = sa.Table(
    "hackers",
    meta,
    sqlalchemy.Column("id", sa.BigInteger, primary_key=True, nullable=False),
    sqlalchemy.Column("level", sa.BigInteger, nullable=False, server_default="0"),
)

ENGINE = None


async def prepare_engine():
    global ENGINE  # reuse connection
    if ENGINE is None:
        ENGINE = Database(DATABASE_URL)
        await ENGINE.connect()
    return ENGINE

