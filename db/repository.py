from db.model import Base

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class dbConnectivity():

    def create_engine_and_session():
        DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return engine, session