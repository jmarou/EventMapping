import random
from typing import Any

import geocoder


def calc_location(text: str) -> str:
    """
    Gets the tweet's plain text and returns the location as WKT 
    (POINT(lng lat)).

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    location : str
        The geolocation as WKT (Well known text).
    """

    # TODO: Have to find better way to extract location!
    capital_words = get_capital_words(text)

    geo = geocoder.osm(capital_words)
    # The tween has to be inside Greece!
    if geo.country_code == "gr":
        # add a slight randomness to the location to avoid two markers on leaflet to overlap 100%
        return f"SRID=4326;POINT({geo.lng} {geo.lat + random.random()/1000})"
    
    return None


def get_capital_words(text: str) -> str:
    """
    Extracts only the capital words for text written in Greek and returns them 
    as comma separated string.

    Parameters
    ----------
    text: str
        The input text.
    
    Returns
    ----------
    capital_words: str
        Comma separated capital words.
    """
    for word in text.split()[1:]:
        unicode = ord(word[0])
        if unicode >= 913 and unicode <= 937:
            capital_words = word + ","
    
    return capital_words


def format_text(text: str) -> str:  
    """
    Gets the tweet's plain text and returns a rich text, including http links
    and twitter hashtags.

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    formatted_text : str
        The rich text.
    """

    text_list = text.split(" ")

    for idx, word in enumerate(text_list):
        if word.startswith("http"):
            text_list[idx] = '<a href="{}">{}</a>'.format(word, word)
        elif word.startswith("#"):
            text_list[idx] = '<a href="https://twitter.com/hashtag/{}">{}</a>'.format(
                word[1:], word
            )
        else:
            pass
    formatted_text = " ".join(text_list)

    return formatted_text


def format_geojson(query_result: Any) -> str:
    """Returns filtered query results as a geojson.""" 
    geojson = ""
    for tweet in query_result:
        geojson += tweet[0] + ","
    
    return (
        '{"type": "FeatureCollection","features": ['
        + geojson[:-1]
        + '], "crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::4326"}}}'
    )
