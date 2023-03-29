import os

from sqlmodel import Session, create_engine

USER = os.getenv("DB_USER", default="root")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", default="127.0.0.1")
PORT = os.getenv("DB_PORT", default=3306)
DATABASE = os.getenv("DB_NAME", default="rpl")

URL = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(USER, PASSWORD, HOST, PORT, DATABASE)

engine = create_engine(URL)


def get_db():
    with Session(engine) as session:
        yield session


# This class is designed for use in the Service and Repository levels
# to facilitate the passing of the DB Session from the FastAPI Router level.
#
# This is necessary because the DB Session is injected in the Router level,
# and the way of getting the DB Session to the Repository level is passing
# it through the function tree.
#
# More info:
# - https://github.com/tiangolo/fastapi/issues/2894
# - https://github.com/tiangolo/fastapi/pull/5489
class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db
