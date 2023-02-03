import os 
import re
from typing import Any

from deepl import Translator
import geocoder
import geograpy 
import spacy

from tokens import DEEPL_TOKEN

DEFAULT_PATTERN = re.compile((
"(\\b(επάνω |"
"νότιας |βόρειας |ανατολικής |δυτικής |"
"[λ|Λ]εωφόρο |[ν|Ν]ομού |νομούς.* και |νομών.* και |πλατείας? |σταθμό |"
"νήσου |λίμνη |Π.Υ. |Π.Ε. |Δ.Ε. |Ε.Ο. |T.K. |"
"οδό |οδού |οδών.*και |δασάκι |φαράγγι (?:του|της|των )?|"
"(?:περιοχής? )|δήμο (?:του|της )?|δήμου |"
"(?:δημοτική )?(?:κοινότητα|ενότητα )|"
"(?:στ[η|ο]ν? )|(?:στα )|(?:στ[ι|ου]ς )|(?:του? )|(?:τη[ς|ν]? )|(?:των ))"
"((?:[Α-ΩΆΈΊΎΏΉΌ][α-ωάέύίόώήϊΐϋ]{0,1}\.\s)+|"
"(?:[Α-ΩΆΈΊΎΏΉΌ0-9]{1,2}[α-ωάέύίόώήϊΐϋ]{2,}\s?)+)+)"
))

TRANSLATOR = Translator(auth_key=DEEPL_TOKEN, skip_language_check=True)
NLP_MODEL = spacy.load("el_core_news_lg") # el_core_news_sm

def regex_woi(text: str, pattern: re.compile = DEFAULT_PATTERN) -> str:
    """
    Gets text and returns key phrases containing location information. 
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
                        # "επί |της |του? |στον? |στην? |στα |στους |την? |"
        woi = re.sub(pattern=re.compile(
                        "\\b(στ[η|ο]ν? |στα |στ[ι|ου]ς |του? |τη[ς|ν]? |των |"
                        "περιοχής?|"
                        "Πυροσβεστικ(?:ού|ό)|Σώμα(?:τος)?|Πολεμικής?|Αεροπορίας?|"
                        "Ομάδας?|Δίωξης?|Τμήμα(?:τος|τα)?|Ασφαλείας?|Ασφάλειας?|Ναρκωτικών|"
                        "Διεύθυνσης?|Αστυνομικ(?:ό|ού|ός)|Νόμο(?:υ|ς)?|Αστυνομίας?|Οικονομικής?)"),
                      repl= "",
                      string=woi).strip()
        if woi.isspace():
            return None
        else:
            return woi
    else:
        return None


def nlp_woi(text: str) -> str:
    """
    Gets text and returns key phrases containing location information. 
    The search is based natural processing language mdoels.

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
    # tokenize
    doc = NLP_MODEL(text)
    ents = doc.ents
    return " ".join([entity.text for entity in ents if entity.label_=='GPE' or entity.label_=='LOC'])


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
    return TRANSLATOR.translate_text(text=text, source_lang='EL',
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
    capital_words = []
    sentences = text.split('. ')
    for sentence in sentences:
        # for every full sentence check all the words, except the first one
        for word in sentence.split()[1:]:
            unicode = ord(word[0])
            # 902: Ά, 904-937: Έ, Ή, ..., Α, Β, Γ, ..., Ω
            if unicode == 902 or (unicode>=904 and unicode <=937):
                capital_words.append(word)
    
    return " ".join(capital_words)
  

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
    # |https?://[\w.\/]*
    text = re.sub(r'(<a href="https?://[\w\.,\/]*">#?)|(https?://[\w\/\.]*</a>)|(</a>)', "", text)
    # place period when missing before newline character
    text = re.sub(r' *?\.?\n', '.\n', text)
    # &amp; is special symbol for '&' in html, but for plain text is not needed
    text = re.sub(r'&amp;', 'και', text)
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
        # non-mappabe events (announcements, re-tweets, etc.)
        if re.search('τελευταίο 24ωρο', plain_text):
            return -1
        elif re.match('rt ', plain_text):
            return -3
        
        # mappable events (fire, rescue, transportation, operations)
        elif re.search('κατάσβεσης?|κατεσβέσθη|κατασβέσθη', plain_text):
            return 1
        elif re.search('στην? πυρκαγιά|υπό (?:μερικό |πλήρη |)έλεγχο|πυρκαγιά σε',
                      plain_text):
            return 2
        elif re.search('ανάσυρσης?|ανασύρθηκ(?:ε|αν)', plain_text):
            return 3
        elif re.search('απεγκλωβίστηκ(?:ε|αν)|απεγκλωβισμός?|μεταφορά|μεταφέρθηκ(?:ε|αν)|'
                       'αεροδιακομιδή|εντοπίστηκ(?:ε|αν)|εντοπισμός?|διασώθηκ(?:ε|αν)',
                      plain_text):
            return 4
        elif re.search('έρευνας? και διάσωσης?|επιχείρησης?|επιχειρούν|επιχείρησαν',
                       plain_text):
            return 5
        # announcement but without event
        elif re.search('δελτίο τύπου', plain_text):
            return -2
        else:
            return 0
    elif department.lower() == 'police':
        # non-mappable events (announcements, traffic, re-tweets, cyber crime)
        if re.search('δενξεχνάμε|σαν[η|ή]μερα', plain_text):
            return -2
        elif re.match('rt ', plain_text):
            return -3
        elif re.search('κυκλοφοριακές ρυθμίσεις|κυκλοφορίας?|ενημερωθείτε για την κίνηση', plain_text):
            return -4
        elif re.search('ηλεκτρονικού εγκλήματος', plain_text):
            return -1
        # mappable events (arrest, crime resolve)
        elif re.search('συνελήφθ(?:η|ησαν|ηκε)|εξαρθρώθηκε|εξάρθρωση', plain_text):
            return 1
        elif re.search('εξιχνιά(?:σ[θ|τ]ηκε|σ[τ|θ]ηκαν)|[εξα|δια]κριβώθηκε|εξακρίβωση', plain_text):
            return 2

        else:
            return 0
    else:
        raise ValueError
