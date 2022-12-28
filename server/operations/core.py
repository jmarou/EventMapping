import os 
import re
from typing import Any, Union, List

import geocoder
import geograpy 
from deepl import Translator

from tokens import DEEPL_TOKEN

DEFAULT_PATTERN = re.compile((
"(\\b(επάνω |"
"νότιας |βόρειας |ανατολικής |δυτικής |"
"λεωφόρο |[ν|Ν]ομού |νομούς.* και |νομών.* και |στο κέντρο (?:της|του )?|"
"νήσου |λίμνη |Π.Υ. |Π.Ε. |Δ.Ε. |Ε.Ο. |"
"|στην οδό |οδού |οδών.*και |δασάκι |"
"περιοχής? |περιοχής? της |στον? δήμο (?:του|της )?|(?:του )?δήμου |"
"(?:δημοτική )?(?:κοινότητα|ενότητα) |"
"στην? |στον? |στα |στους |στις |του |της |το |την? )"
"((?:[Α-ΩΆΈΊΎΏΉΌ][α-ωάέύίόώήϊΐϋ]{0,1}\.\s)+|"
"(?:[Α-ΩΆΈΊΎΏΉΌ0-9]{1,2}[α-ωάέύίόώήϊΐϋ]{2,}\s?)+)+)"
))

translator = Translator(auth_key=DEEPL_TOKEN, skip_language_check=True)


def find_woi_in_text(text: str, pattern: re.compile = DEFAULT_PATTERN)\
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
        woi = " ".join([(match[0].strip()) for
                         match in m if match[1]!=""])
        return re.sub(pattern=re.compile((
                        "επί |της |του? |στον? |στην? |στα |στους |την? |"
                        "Πυροσβεστικού Σώματος\s?|Πολεμικής Αεροπορίας\s?")),
                      repl= "",
                      string=woi).strip()
    else:
        return ''


def translate_text(text: str) -> str:
    """
    Gets the text of the tweet (greek) and translates it to english
    using the deepL API.

    Parameters
    ----------
    text: str
        The input text.
    
    Returns
    ---------- 
    _: str
        The translated in english tweet text.
    """
    if text == "":
        return ""
    return translator.translate_text(text=text, source_lang='EL',
                                     target_lang='EN-US').text


def calc_location(text: str) -> str:
    """
    Gets a text including words or phrases describing geographic locations 
    (words of interest) and returns the latitude, longitude from the geocoder.

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    location : str
        The geolocation as WKT (Well known text).
    """
    geo = geocoder.osm(text)
    # The tween has to be inside Greece!
    if geo.country_code == "gr":
        # add a slight randomness to the location to avoid two markers on leaflet to overlap 100%
        return geo.lng, geo.lat
        # return f"SRID=4326;POINT({geo.lng} {geo.lat + random.random()/1000})"
    
    return None, None


def format_geojson(query_result: Any) -> str:
    """Returns filtered query results as a geojson.""" 
    geojson = ""
    for tweet in query_result:
        geojson += tweet.__repr__() + ","
    
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


def geograpy_woi(text: str) -> str:
    """
    Taken a translated (in english) tweet text, returns the words containing
    location information using the geograpy3 library.

    Parameters
    ----------
    text: str
        The input text already translated to english. Geograpy3 doesn't support
        the greek language.
    
    Returns
    ---------- 
    words of interest: str
        Key phrases/words that contain location information. These are 
        joined by spaces. If nothing is found returns an empty string.
    """
    if text == "":
        return ""
    extractor = geograpy.extraction.Extractor(text=text)
    wois = extractor.find_geoEntities()
    if wois == []:
        return ""

    return ", ".join(wois)
