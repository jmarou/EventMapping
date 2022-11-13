import random
import re
from typing import Any

import geocoder
import pandas as pd 

default_pattern = re.compile((
"(?:(?:νότιας )|(?:βόρειας )|(?:ανατολικής )|(?:δυτικής )|"
"(?:στην? Λ. )|(?:λεωφόρο )|(?:[ν|Ν]ομού )|(?:στο κέντρο της )|(?:κέντρου? )|"
"(?:νήσου )|(?:λίμνη )|(?:Π.Υ. )|(?:(?:της )? Π.Ε. )|"
"(?:επί της )|(?:επί της οδού )|(?:στην οδό )|(?:οδού )|"
"(?:στην? περιοχή )|(?:περιοχής της )|"
"(?:στον? δήμο )|(?:(?:του )?δήμου )?|"
"(?:στην? )|(?:στα )|(?:στους )|(?:στον? )|"
"(?:(?:του|της ))|"
"(?:(?:δημοτική )?(?:κοινότητα|ενότητα) ))"
"(?:(?:[Α-ΩΆΈΊΎΏΉΌ]|(?:\d+))[α-ωάέύίόώήϊΐϋ.]+\s?)+"), flags=re.I)


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


def find_woi_in_text(text: str, pattern: re.compile = default_pattern)\
    -> str:
    """
    Given an input text returns key phrases containing location information. The
    search is based on regular expression matching.

    Parameters
    ----------
    text: str
        The input text.
    
    Returns
    ---------- 
    words of interest: str
        Key phrases/words that contain location information. These are 
        joined by spaces. If nothing is found returns an empty string.
    """

    m = re.findall(pattern=pattern, string=text)
    if m:
        return " ".join([match.rstrip() for match in m])
    else:
        return ''


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
    capital_words = ""
    for word in text.split()[1:]:
        unicode = ord(word[0])
        if unicode >= 913 and unicode <= 937:
            capital_words = word + ","
    
    return capital_words
  

def remove_links_emojis(text):
    """Gets the tweet's plain text and returns the same texting without the html 
    links (<a href=url></a>) and without hashtags.

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    formatted_text : str
        The tweet text wihtout html links and/or hashtags.
    """
    # TODO: Optimize this function for better regex!
    # remove the href links
    text = re.sub(r'<a href=[\'"]?[^>]+>', '', text)
    text = re.sub(r'</a>', '', text)
    # remove hashtags
    text = re.sub('#', '', text)
    # remove any remaining links from the text
    text = re.sub("https?://.*", '', text)
    # remove anything that is not word, whitespace, comma or period (emojis)
    return re.sub(r'[^\w\s,.]', '', text)  
