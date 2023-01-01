import os 
import re
from typing import Any

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


def find_woi_in_text(text: str, pattern: re.compile = DEFAULT_PATTERN) -> str:
    """
    Given an input text returns key phrases containing location information. 
    The search is based on regular expression matching.

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
                        "Πυροσβεστικού Σώματος\s?|Πολεμικής Αεροπορίας\s?|"
                        "Ομάδας?|Διώξης?|")),
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
    as space separated string.

    Parameters
    ----------
    text: str
        The input text.
    
    Returns
    ----------
    capital_words: str
        Space separated capital words.
    """
    capital_words = re.findall(pattern='[Α-ΩΆΈΊΎΏΉΌ][α-ωάέύίόώήϊΐϋ]+', string=text)
    if capital_words: 
        return " ".join([word for word in capital_words[1:]])
    return ""    
    
  

def remove_links_emojis(text):
    """
    Gets the tweet's plain text and returns the same texting without the html
    links (<a href=url></a>), hashtags (#) and emojis

    Parameters
    ----------
    text : str
        The input text (rich format)

    Returns
    ----------
    formatted_text : str
        The tweet text wihtout html links, hashtags and emojis
    """
    # REMOVE ALL LINKS AND HASHTAGS
    text = re.sub(r'(<a href="https?://[\w\.\/]*">#?)|(https?://[\w\/\.]*</a>)|(</a>)', "", text)
    # place period when missing before newline character
    text = re.sub(r' *?\.?\n', '.\n', text)
    # remove anything that is not word, whitespace, comma or period (emojis)
    text = re.sub(r'[^\w\s,.]', ' ', text)
    # replace double (or more) spaces with single space
    return re.sub(r' {2,}', ' ', text)


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


def categorize_tweet(plain_text: str, department: str) -> int:
    """
    Takes the plain text (no links, hashtags or emojis) of a tweet
    and returns an integer based on the category map.

    Parameters
    ----------
    plain_text: str
       The plain text (no links, hashtags or emojis) of a tweet.
    department: str
        The name of the department the tweet comes from. 'Pyrosvestiki'
        or 'Police'.

    Returns
    ---------- 
    category: int
        An integer representing the category of the tweet.
    """
    plain_text = plain_text.lower()
    if department.lower() == 'pyrosvestiki':
        if re.search('ανάσυρσης?|ανασύρθηκ(?:ε|αν)', plain_text):
            return 0
        elif re.search('απεγκλωβίστηκ(?:ε|αν)|απεγκλωβισμός?|μεταφορά|μεταφέρθηκ(?:ε|αν)',
                      plain_text):
            return 1
        elif re.search('εντοπίστηκ(?:ε|αν)|εντοπισμός?|διασώθηκ(?:ε|αν)|αεροδιακομιδή', plain_text):
            return 2
        elif re.search('κατάσβεσης?|κατεσβέσθη|κατασβέσθη', plain_text):
            return 3
        elif re.search('πυρκαγιά|στην? πυρκαγιά|υπό (?:μερικό|πλήρη )?έλεγχο',
                      plain_text):
            return 4
        elif re.search('έρευνας? και διάσωσης?|επιχείρησης?|επιχειρούν|επιχείρησαν',
                       plain_text):
            return 5
        elif re.search('τελευταίο 24ωρο', plain_text):
            return -1
        elif re.search('δελτίο τύπου', plain_text):
            return -2
        else:
            return -3
    elif department.lower() == 'police':
        if re.search('συνελήφθ(?:η|ησαν|ηκε)', plain_text):
            return 0
        elif re.search('εξιχνιάσ(?:σθηκε|στηκαν)|εξακριβώθηκε|εξαρθρώθηκε', plain_text):
            return 1
        elif re.search('δενξεχνάμε', plain_text):
            return -1
        elif re.search('σανσήμερα', plain_text):
            return -2
        elif re.search('κυκλοφοριακές ρυθμίσεις', plain_text):
            return -3
        elif re.match('RT ', plain_text):
            return -4
        else:
            return -5
    else:
        raise ValueError
