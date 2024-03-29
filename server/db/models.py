import json
from datetime import datetime

from sqlalchemy import Column, String, DateTime, BIGINT, Float, INTEGER

from db.database import Base, engine


EVENTS_DICT = {
    "pyrosvestiki": {
        -4: "Δελτίο Τύπου",
        -3: "Retweet",
        -2: "#ΣανΣήμερα-#ΔενΞεχνάμε",
        -1: "Εξέλιξη τελευταίου 24ωρου",
        0: "Διάφορα",
        1: "Κατάσβεση πυρκαγιάς",
        2: "Ενημέρωση πυρκαγιάς",
        3: "Ανάσυρση ατόμου",
        4: "Απεγκλωβισμός-Εντοπισμός-Διάσωση",
        5: "Επιχείρηση έρευνας & διάσωσης",
    },
    "police": {
        -4: "Κυκλοφοριακές ρυθμίσεις-κίνηση",
        -3: "Retweet",
        -2: "#ΣανΣήμερα-#ΔενΞεχνάμε",
        -1: "Ηλεκτρονικό έγκλημα",
        0: "Διάφορα",
        1: "Σύλληψη-εξάρθρωση",
        2: "Εξιχνίαση-εξακρίβωση υπόθεσης",
        3: "Εντοπισμός",
    },
}


def get_geojson(
    id: int,
    text: str,
    created_at: datetime,
    latitude: Float,
    longitude: Float,
    category: str,
) -> json:
    geojson = {"type": "Feature"}
    geojson["properties"] = {
        "id": str(id),  # id > javascript highest integer value
        "created_at": created_at.strftime("%d/%m/%Y, %H:%M:%S"),
        "text": text,
        "category": category,
    }
    geojson["geometry"] = {
        "type": "Point",
        "coordinates": [latitude, longitude],
    }
    return json.dumps(geojson)


class PyrosvestikiTweets(Base):
    """DB model for pyrosvestiki tweets."""

    __tablename__ = "pyrosvestikitweets"

    id = Column("id", BIGINT, primary_key=True)
    text = Column("text", String)
    created_at = Column("created_at", DateTime)
    plain_text = Column("plain_text", String)
    category = Column("category", INTEGER)
    translated_text = Column("translated_text", String)
    regex_woi = Column("regex_woi", String)
    capital_words = Column("capital_words", String)
    geograpy_woi = Column("geograpy_woi", String)
    spacy_woi = Column("spacy_woi", String)
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)

    def __init__(
        self,
        id,
        text,
        created_at,
        plain_text,
        category,
        translated_text,
        regex_woi,
        capital_words,
        geograpy_woi,
        spacy_woi,
        latitude=None,
        longitude=None,
    ):
        self.id = id
        self.text = text
        self.created_at = created_at
        self.plain_text = plain_text
        self.category = category
        self.translated_text = translated_text
        self.regex_woi = regex_woi
        self.capital_words = capital_words
        self.geograpy_woi = geograpy_woi
        self.spacy_woi = spacy_woi
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return get_geojson(
            self.id,
            self.text,
            self.created_at,
            self.latitude,
            self.longitude,
            EVENTS_DICT["pyrosvestiki"][self.category],
        )


class PoliceTweets(Base):
    """DB model for police tweets."""

    __tablename__ = "policetweets"

    id = Column("id", BIGINT, primary_key=True)
    text = Column("text", String)
    created_at = Column("created_at", DateTime)
    plain_text = Column("plain_text", String)
    category = Column("category", INTEGER)
    translated_text = Column("translated_text", String)
    regex_woi = Column("regex_woi", String)
    capital_words = Column("capital_words", String)
    geograpy_woi = Column("geograpy_woi", String)
    spacy_woi = Column("spacy_woi", String)
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)

    def __init__(
        self,
        id,
        text,
        created_at,
        plain_text,
        category,
        translated_text,
        regex_woi,
        capital_words,
        geograpy_woi,
        spacy_woi,
        latitude=None,
        longitude=None,
    ):
        self.id = id
        self.text = text
        self.created_at = created_at
        self.plain_text = plain_text
        self.category = category
        self.translated_text = translated_text
        self.regex_woi = regex_woi
        self.capital_words = capital_words
        self.geograpy_woi = geograpy_woi
        self.spacy_woi = spacy_woi
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return get_geojson(
            self.id,
            self.text,
            self.created_at,
            self.latitude,
            self.longitude,
            EVENTS_DICT["police"][self.category],
        )


def create_DB_tables():
    """Run this function to create the tables in postgresql."""
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_DB_tables()
