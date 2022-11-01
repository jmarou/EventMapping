from geoalchemy2 import Geometry, functions
from shapely import wkb
from sqlalchemy import (
    Column,
    String,
    DateTime,
    BIGINT,
)

from db.database import Base, engine


class PyrosvestikiTweets(Base):
    """DB model for pyrosvestiki tweets."""
    __tablename__ = "pyrosvestikitweets"

    id = Column("id", BIGINT, primary_key=True)
    text = Column("text", String)
    created_at = Column("created_at", DateTime)
    location = Column("location", Geometry(geometry_type="POINT", srid=4326))

    def __init__(self, id, text, created_at, location="SRID=4326;POINT(0 0)"):
        self.id = id
        self.text = text
        self.created_at = created_at
        self.location = location

    def __repr__(self):
        return """
        {"type": "Feature",
        "properties": {
            "id": %s, 
            "created_at": %s
            },
        "geometry": {
            "type": "Point",
            "coordinates": [%s]
            }
        }
        """ % (
            self.id,
            self.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
            wkb.loads(self.location, hex=True),
        )


class PoliceTweets(Base):
    """DB model for police tweets."""
    __tablename__ = "policetweets"

    id = Column("id", BIGINT, primary_key=True)
    text = Column("text", String)
    created_at = Column("created_at", DateTime)
    location = Column("location", Geometry(geometry_type="POINT", srid=4326))

    def __init__(self, id, text, created_at, location="SRID=4326;POINT(0 0)"):
        self.id = id
        self.text = text
        self.created_at = created_at
        self.location = location

    def __repr__(self):
        return """
        {"type": "Feature",
        "properties": {
            "id": %s, 
            "created_at": %s
            },
        "geometry": {
            "type": "Point",
            "coordinates": [%s]
            }
        }
        """ % (
            self.id,
            self.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
            functions.ST_GeomAsText(self.location),
        )


def create_DB_tables():
    """Run this function to create the tables in postgresql."""
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_DB_tables()
