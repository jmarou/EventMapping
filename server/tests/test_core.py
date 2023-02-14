import unittest

from operations.core import (
    remove_links_emojis,
    translate_text,
    geograpy_woi,
    capital_words,
    regex_woi,
    spacy_woi,
    geocoding_osm,
    geocoding_esri,
)


class testOperationsCore(unittest.TestCase):
    @classmethod
    def setUp(self):
        # threshold for distance of geocoding result in meters
        self.geocode_threshold = 500

        # tests for geocoders
        self.address1 = "Βαλτόνερα"
        self.geocode1 = (21.58558000000005, 40.636810000000025)

        # original text from tweets
        self.tweet1 = (
            'Κατεσβέσθη <a href="https://twitter.com/hashtag/πυρκαγιά">#πυρκαγιά</a> σε κεραμοσκεπή οικίας, στο δήμο Κατερίνης Πιερίας.'
            '🚒🚒Επιχείρησαν 15 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με 5 οχήματα.'
        )
        self.tweet2 = (
            "Σε εξέλιξη επιχείρηση ανάσυρσης ατόμου από αμαξοστοιχία τρένου στο Κρυονέρι Αττικής."
            '🚒🚒Επιχειρούν 6 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με 2 οχήματα.'
            '<a href="https://t.co/5JSKRCC7Bt">https://t.co/5JSKRCC7Bt</a>'
        )
        self.tweet3 = (
            'Ολοκληρώθηκε ο <a href="https://twitter.com/hashtag/απεγκλωβισμός">#απεγκλωβισμός</a> τραυματισμένου'
            " ατόμου  από Ε.Ι.Χ. αυτοκίνητο και"
            " παραδόθηκε στο ΕΚΑΒ, συνεπεία τροχαίου, στη Δ.Ε. Παλιανής (διαστάυρωση Άγιος Θωμάς) Ηρακλείου Κρήτης."
            ' Επιχείρησαν 9 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με 3 οχήματα.'
        )
        self.tweet4 = (
            'Κατεσβέσθη <a href="https://twitter.com/hashtag/πυρκαγιά">#πυρκαγιά</a> σε μονοκατοικία στην'
            " Τ.Κ.  Φανού, στο δήμο Αμύνταιου, Φλώρινας. "
            '🚒🚒🚒Επιχείρησαν 6 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με 3 οχήματα.'
            ' <a href="https://t.co/azGG4qMUwk">https://t.co/azGG4qMUwk</a>'
        )
        self.tweet5 = (
            '<a href="https://twitter.com/hashtag/Πυρκαγιά🔥">#Πυρκαγιά🔥</a> σε αγροτοδασική έκταση στην Δ.Ε.'
            ' Ιεράπετρας Κρήτης. Άμεσα κινητοποιήθηκαν 30 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με'
            " 11 οχήματα 🚒🚒🚒 και 1 ομάδα πεζοπόρου τμήματος. Συνδρομή από υδροφόρες Ο.Τ.Α."
        )
        self.tweet6 = (
            "Οδηγίες της Ελληνικής Αστυνομίας για την αντιμετώπιση της ενδοοικογενειακής βίας. "
            'Βρείτε βοήθεια εδώ:  <a href="https://t.co/r5UWpGWZ4e'
            "#ExeisFoni"
            "#MenoumeAsfaleis"
            '🎥">https://t.co/r5UWpGWZ4e'
            "#ExeisFoni"
            "#MenoumeAsfaleis"
            '🎥</a> <a href="https://t.co/rrXIIdhXxA">https://t.co/rrXIIdhXxA</a>'
        )
        self.tweet7 = (
            "Από αστυνομικούς του Τμήματος Ασφαλείας Χαλκίδας, συνελήφθη ένα άτομο, διότι σε ειδική κρύπτη του οχήματός του, εντοπίστηκαν 11 κιλά ηρωίνης."
            "▪Η σύλληψή του πραγματοποιήθηκε, μετά από καταδίωξη, στη Νέα Εθνική Οδό Αθηνών- Λαμίας."
            "➡https://t.co/cv4Q5Bq7Fj"
            "https://t.co/JzeY8yJhpH"
        )

        # plain text from tweets (links, emojis, commas are removed)
        self.plain_text1 = (
            "Κατεσβέσθη πυρκαγιά σε κεραμοσκεπή οικίας στο δήμο Κατερίνης Πιερίας."
            " Επιχείρησαν 15 πυροσβέστες με 5 οχήματα."
        )
        self.plain_text2 = (
            "Σε εξέλιξη επιχείρηση ανάσυρσης ατόμου από αμαξοστοιχία τρένου στο Κρυονέρι Αττικής."
            " Επιχειρούν 6 πυροσβέστες με 2 οχήματα."
        )
        self.plain_text3 = (
            "Ολοκληρώθηκε ο απεγκλωβισμός τραυματισμένου ατόμου από Ε.Ι.Χ. αυτοκίνητο και παραδόθηκε"
            " στο ΕΚΑΒ συνεπεία τροχαίου στη Δ.Ε. Παλιανής διαστάυρωση Άγιος Θωμάς Ηρακλείου Κρήτης."
            " Επιχείρησαν 9 πυροσβέστες με 3 οχήματα."
        )
        self.plain_text4 = (
            "Κατεσβέσθη πυρκαγιά σε μονοκατοικία στην Τ.Κ. Φανού στο δήμο Αμύνταιου Φλώρινας."
            " Επιχείρησαν 6 πυροσβέστες με 3 οχήματα."
        )
        self.plain_text5 = (
            "Πυρκαγιά σε αγροτοδασική έκταση στην Δ.Ε. Ιεράπετρας Κρήτης. Άμεσα"
            " κινητοποιήθηκαν 30 πυροσβέστες με 11 οχήματα και 1 ομάδα πεζοπόρου τμήματος."
            " Συνδρομή από υδροφόρες Ο.Τ.Α."
        )
        self.plain_text6 = (
            "Οδηγίες της Ελληνικής Αστυνομίας για την αντιμετώπιση της ενδοοικογενειακής βίας."
            " Βρείτε βοήθεια εδώ"
        )
        self.plain_text7 = (
            "Από αστυνομικούς του Τμήματος Ασφαλείας Χαλκίδας συνελήφθη ένα άτομο διότι σε ειδική κρύπτη"
            " του οχήματός του εντοπίστηκαν 11 κιλά ηρωίνης. Η σύλληψή του πραγματοποιήθηκε μετά από"
            " καταδίωξη στη Νέα Εθνική Οδό Αθηνών Λαμίας."
        )

        # translated plain text from tweet (using deepL)
        self.translated1 = (
            "Operation to rescue a person from a train in Kryoneri, Attica"
        )

    def test_remove_links_emojis(self):
        self.maxDiff = None
        self.assertEqual(remove_links_emojis(self.tweet1), self.plain_text1)
        self.assertEqual(remove_links_emojis(self.tweet2), self.plain_text2)
        self.assertEqual(remove_links_emojis(self.tweet3), self.plain_text3)
        self.assertEqual(remove_links_emojis(self.tweet4), self.plain_text4)
        self.assertEqual(remove_links_emojis(self.tweet5), self.plain_text5)
        self.assertEqual(remove_links_emojis(self.tweet6), self.plain_text6)
        self.assertEqual(remove_links_emojis(self.tweet7), self.plain_text7)
        self.assertEqual(remove_links_emojis(""), "")

    def test_translate_text(self):
        text = self.tweet2.split(".")[0]
        self.assertEqual(translate_text(text), self.translated1)

    def test_geograpy_woi(self):
        self.assertEqual(geograpy_woi(self.translated1), "Kryoneri")

    def test_capital_words(self):
        self.assertEqual(
            capital_words(self.plain_text1), "Κατερίνης Πιερίας"
        )
        self.assertEqual(
            capital_words(self.plain_text4), "Φανού Αμύνταιου Φλώρινας"
        )

    def test_regex_woi(self):
        tweet1 = (
            "Κατεσβέσθη πυρκαγιά σε Ι.Χ.Ε. όχημα επί της Λεωφ. Βασιλίσσης "
            "Σοφίας στον δήμο Αθηναίων. Επιχείρησαν 6 πυροσβέστες με 2 οχήματα."
        )
        self.assertEqual(regex_woi(tweet1), "Βασιλίσσης Σοφίας Αθηναίων")
        self.assertEqual(regex_woi(self.plain_text3), "Παλιανής")
        self.assertEqual(regex_woi(self.plain_text5), "Ιεράπετρας Κρήτης")
        self.assertEqual(
            regex_woi(self.plain_text4), "Φανού Αμύνταιου Φλώρινας"
        )

    def test_spacy_woi(self):
        pass

    def test_geocoding_esri(self):
        self.assertLess

    def test_geocoding_osm(self):
        address1 = "Βαλτόνερα"
        pass


if __name__ == "__main__":
    unittest.main()
