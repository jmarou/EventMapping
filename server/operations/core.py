import re
from typing import Any, Tuple

from arcgis.geocoding import geocode
from arcgis.gis import GIS
from deepl import Translator
import geocoder
import geograpy
import geopy.distance
import googlemaps
import spacy
import urllib3

from tokens import DEEPL_TOKEN, ARCGIS_TOKEN, GOOGLE_TOKEN

urllib3.disable_warnings()

DEFAULT_PATTERN = re.compile(
    (
        "(\\b(επάνω |"
        "νότιας? |βόρειας? |ανατολικής? |δυτικής? |κέντρο |"
        "(?:[λ|Λ]εωφόρου? )|(?:(?:της )?Λεωφ. )|[ν|Ν]ομού |νομούς.* και |νομών.* και |πλατείας? |σταθμό |"
        "νήσου? |λίμνης? |Π.Ε. |Δ.Ε. |Ε.Ο. |Π.Ε.Ο. |Τ.Κ. |"
        "οδό |οδού |οδών.*και |δασάκι |φαράγγι (?:του|της|των )?|"
        "περιοχής? |(?:[Δ|δ]ήμο του|της )?|(?:[Δ|δ]ήμου?) |οικισμ[ό|ού] |"
        "(?:δημοτική )?(?:κοινότητα|ενότητα )|"
        "(?:στ[η|ο]ν? )|(?:στα )|(?:στ[ι|ου]ς )|(?:του? )|(?:τη[ς|ν]? )|(?:των ))"
        "((?:[Α-ΩΆΈΊΎΏΉΌ][α-ωάέύίόώήϊΐϋ]{0,1}\.\s)+|"
        "(?:[Α-ΩΆΈΊΎΏΉΌ0-9]{1,2}[α-ωάέύίόώήϊΐϋ]{2,}\s?)+)+)"
    )
)

NOT_PATTERN = re.compile(
    "Πολεμική|Αεροπορία|Σώμα|Πυροσβεστ|Δίωξη|Αστυνομία|Τμήμα|"
    "Δίωξη|Υπηρεσία|Νομοθεσία|Νόμο|Ασφάλεια|Ασφαλείας|Διεύθυνση|"
    "Αντιτρομοκρατική|Ναρκωτικ"
)

TRANSLATOR = Translator(auth_key=DEEPL_TOKEN, skip_language_check=True)
NLP_MODEL = spacy.load("el_core_news_lg")  # el_core_news_sm

gis = GIS(api_token=ARCGIS_TOKEN, verify_cert=False)
gmaps = googlemaps.Client(key=GOOGLE_TOKEN)


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
    # match everything using the pattern
    m_all = re.findall(pattern=pattern, string=text)
    # discard any match that includes part of the NOT_PATTERN
    m = [match for match in m_all if not re.search(NOT_PATTERN, match[0])]
    if m:
        # join all the finds using the fullmatch and not the groups
        woi = " ".join([(match[0].strip()) for match in m if match[1] != ""])
        # remove any unwanted part that doesn't contribute to geocoding
        woi = re.sub(
            pattern=re.compile(
                "\\b(στ[ηο]ν? |στα |στ(ι|ου)ς |του? |τη[ςν]? |των |"
                "Δ.Ε.? |Π.Υ.? |Π.Ε.Ο.? |Ε.Ο.? |Τ.Κ. |"
                "περιοχής?|οδών |Λεωφ. |δήμου? |οδ(ό|ού) |Λεωφόρου? |[Νν]ομ(ός?|ού) )"
            ),
            repl="",
            string=woi,
        ).strip()
        if woi.isspace():
            return None
        else:
            return woi.strip()
    else:
        return None


def spacy_woi(text: str) -> str:
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
    woi = " ".join(
        [
            entity.text
            for entity in ents
            if entity.label_ == "GPE" or entity.label_ == "LOC"
        ]
    )
    if woi.isspace():
        return None
    return re.sub(
        pattern=re.compile(
            "\\b(Δ.Ε.? |Π.Υ.? |T.K.? |Π.Ε.Ο.? |Ε.Ο.? |"
            "περιοχής?|οδών |και |Λεωφ. |δήμου? |οδ(ό|ού) |Λεωφόρου? |"
            "Πυροσβεστικ(?:ού|ό)|Σώμα(?:τος)?|Πολεμικής?|Αεροπορίας?|"
            "Ομάδας?|Δίωξης?|Τμήμα(?:τος|τα)?|Ασφαλείας?|Ασφάλειας?|Ναρκωτικών|"
            "Διεύθυνσης?|Αστυνομικ(?:ό|ού|ός)|Νόμο(?:υ|ς)?|Αστυνομίας?|Οικονομικής?)"
        ),
        repl="",
        string=woi,
    ).strip()


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
    return TRANSLATOR.translate_text(
        text=text, source_lang="EL", target_lang="EN-US"
    ).text


def geocoding_osm(text: str) -> Tuple:
    """
    Gets a text including words or phrases describing geographic locations
    (words of interest) and returns the latitude, longitude from geocoding.

    NOTE: OSM geocoder (Open Street Map)
    More info: https://nominatim.org

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    latitude: float
        The latitude value in WGS84 (4326)
    longitude: float
        The longitude value in WGS84 (4326)
    """
    # for empty text return None, no need to do a rest call
    if not text:
        return (None, None)
    geo = geocoder.osm(text)
    # The tween has to be inside Greece!
    if geo.country_code == "gr":
        # add a slight randomness to the location to avoid two markers on leaflet to overlap 100%
        # return f"SRID=4326;POINT({geo.lng} {geo.lat + random.random()/1000})"
        return (geo.lng, geo.lat)

    return (None, None)


def geocoding_google(text: str) -> Tuple:
    """
    Gets a text including words or phrases describing geographic locations
    (words of interest) and returns the latitude, longitude from the geocoder.

    NOTE: Google Geocoding API
    More info: https://developers.google.com/maps/documentation/geocoding/overview

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    latitude: float
        The latitude value in WGS84 (4326)
    longitude: float
        The longitude value in WGS84 (4326)
    """
    # for empty text return None, no need to do a rest call
    if not text:
        return (None, None)

    r = gmaps.geocode(text)
    if r:
        # todo check country
        return (
            r[0]["geometry"]["location"]["lng"],
            r.json[0]["geometry"]["location"]["lat"],
        )
    return (None, None)


def geocoding_esri(text: str) -> Tuple:
    """
    Gets a text including words or phrases describing geographic locations
    (words of interest) and returns the latitude, longitude from the geocoder.

    NOTE: ArcGIS World Geocoder
    More info: https://www.esri.com/en-us/arcgis/products/arcgis-world-geocoder

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    latitude: float
        The latitude value in WGS84 (4326)
    longitude: float
        The longitude value in WGS84 (4326)
    """
    # for empty text return None, no need to do a rest call
    if not text:
        return (None, None)
    r = geocode(
        address=text,
        max_locations=1,
        source_country="GRC",
        out_sr="4326",
        # Greece bounding box
        search_extent=(
            20.1500159034,
            34.9199876979,
            26.6041955909,
            41.8269046087,
        ),
    )
    if r:
        # check result is inside Greece otherwise discard it
        if r[0]["attributes"]["Country"] == "GRC":
            return (
                r[0]["attributes"]["DisplayX"],
                r[0]["attributes"]["DisplayY"],
            )

    return (None, None)


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
            text_list[
                idx
            ] = '<a href="https://twitter.com/hashtag/{}">{}</a>'.format(
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
    sentences = [
        re.sub(r"\.$", "", sentence)
        for sentence in re.split(r"(.{2,}?\.)", text)
        if sentence != ""
    ]
    for sentence in sentences:
        # for every full sentence check all the words, except the first one
        for word in sentence.split()[1:]:
            if len(word) < 2:
                continue
            unicode = ord(word[0])
            # 902: Ά, 904-937: Έ, Ή, ..., Α, Β, Γ, ..., Ω
            if unicode == 902 or (unicode >= 904 and unicode <= 937):
                capital_words.append(word)

    return re.sub(",", "", " ".join(capital_words))


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
    text = re.sub(
        r'<a href="https?://[\s\S]*?">#?|https?://[\s\S]*?</a>|https?://[\s\S]*$|</a>',
        "",
        text,
    )
    # remove any newline character (and dot+spaces before it) with single dot
    text = re.sub(r"\.? *\n", ". ", text)
    # &amp; is special symbol for '&' in html, but for plain text is not needed
    text = re.sub(r"&amp;", "και", text)
    # remove anything that is not word, whitespace or period (emojis and commas)
    text = re.sub(r"[^\w\s.]", " ", text)
    # replace double (or more) spaces with single space
    return re.sub(r" {2,}", " ", text.strip())


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
    if text == "" or not text:
        return None
    extractor = geograpy.extraction.Extractor(text=text)
    wois = extractor.find_geoEntities()
    if wois == []:
        return None

    return " ".join(wois)


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
    if department.lower() == "pyrosvestiki":
        # non-mappabe events (announcements, re-tweets, etc.)
        if re.search("τελευταίο 24ωρο", plain_text):
            return -1
        if re.search("δενξεχνάμε|σανσ[η|ή]μερα", plain_text):
            return -2
        elif re.match("rt ", plain_text):
            return -3

        # mappable events (fire, rescue, transportation, operations)
        elif re.search("κατάσβεσης?|κατεσβέσθη|κατασβέσθη", plain_text):
            return 1
        elif re.search(
            "στην? πυρκαγιά|υπό (?:μερικό |πλήρη |)έλεγχο|πυρκαγιά σε",
            plain_text,
        ):
            return 2
        elif re.search("ανάσυρσης?|ανασύρθηκ(?:ε|αν)", plain_text):
            return 3
        elif re.search(
            "απεγκλωβίστηκ(?:ε|αν)|απεγκλωβισμός?|μεταφορά|μεταφέρθηκ(?:ε|αν)|"
            "αεροδιακομιδή|εντοπίστηκ(?:ε|αν)|εντοπισμός?|διασώθηκ(?:ε|αν)",
            plain_text,
        ):
            return 4
        elif re.search(
            "έρευνας? και διάσωσης?|επιχείρησης?|επιχειρούν|επιχείρησαν",
            plain_text,
        ):
            return 5
        # announcement but without event
        elif re.search("δελτίο τύπου", plain_text):
            return -4
        else:
            return 0
    elif department.lower() == "police":
        # non-mappable events (announcements, traffic, re-tweets, cyber crime)
        if re.search("δενξεχνάμε|σανσ[η|ή]μερα", plain_text):
            return -2
        elif re.match("rt ", plain_text):
            return -3
        elif re.search(
            "κυκλοφοριακές ρυθμίσεις|κυκλοφορίας?|ενημερωθείτε για την κίνηση",
            plain_text,
        ):
            return -4
        elif re.search("ηλεκτρονικού εγκλήματος", plain_text):
            return -1
        # mappable events (arrest, crime resolve)
        elif re.search(
            "συνελήφθ(?:η|ησαν|ηκε)|εξαρθρώθηκε|εξάρθρωση|σ[ύ|υ]λληψ[η|εις]",
            plain_text,
        ):
            return 1
        elif re.search(
            "εξιχνιά(?:σ[θ|τ]ηκε|σ[τ|θ]ηκαν)|[εξα|δια]κριβώθηκε|εξακρίβωση",
            plain_text,
        ):
            return 2
        elif re.search("εντοπίσ[τηκε|θηκαν]|εντοπισμός?", plain_text):
            return 3
        else:
            return 0
    else:
        raise ValueError


def get_distance(point_a: Tuple, point_b: Tuple) -> float:
    """
    Calculates the distance in meters for two points in WGS84

    Parameters
    ----------
    point_a: Tuple
       The first Point as a tuple

    point_b: Tuple
       The second Point as a tuple

    Returns
    ----------
    distance: float
        The calculated distance in meters in WGS84 (4326)
    """
    return geopy.distance.geodesic(point_a, point_b).m


def get_geocoding_result(
    point_a: Tuple, point_b: Tuple, threshold: int = 500
) -> int:
    """
    Given two Points and a threshold (distance in meters) returns 1 if distance
    is less than the threshold else returns 0

    Parameters
    ----------
    point_a: Tuple
       The first Point as a tuple

    point_b: Tuple
       The second Point as a tuple

    Returns
    ----------
    int: int
        1 if distance is less than the threshold else 0
    """
    return (
        1 if get_distance(point_a=point_a, point_b=point_b) < threshold else 0
    )
