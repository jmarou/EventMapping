import json
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    BIGINT,
    Float
)

from db.database import Base, engine


def get_geojson(id: int, text: str, created_at: datetime, 
                latitude: Float, longitude: Float) -> json:
    geojson = {"type": "Feature"}
    geojson["properties"] = {
        "id": id,
        "created_at": created_at.strftime("%d/%m/%Y, %H:%M:%S"),
        "text": text
    }
    geojson["geometry"] = {
        "type": "Point",
        "coordinates": [latitude, longitude]
    }
    return json.dumps(geojson)


class PyrosvestikiTweets(Base):
    """DB model for pyrosvestiki tweets."""
    __tablename__ = "pyrosvestikitweets"

    id = Column("id", BIGINT, primary_key=True)
    text = Column("text", String)
    created_at = Column("created_at", DateTime)
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)

    def __init__(self, id, text, created_at, latitude=None, longitude=None): 
        self.id = id
        self.text = text
        self.created_at = created_at
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return get_geojson(self.id, self.text, self.created_at, self.latitude, 
                           self.longitude)


class PoliceTweets(Base):
    """DB model for police tweets."""
    __tablename__ = "policetweets"

    id = Column("id", BIGINT, primary_key=True)
    text = Column("text", String)
    created_at = Column("created_at", DateTime)
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)

    def __init__(self, id, text, created_at, latitude=None, longitude=None):
        self.id = id
        self.text = text
        self.created_at = created_at
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return get_geojson(self.id, self.text, self.created_at, self.latitude, 
                           self.longitude)


def create_DB_tables():
    """Run this function to create the tables in postgresql."""
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_DB_tables()
