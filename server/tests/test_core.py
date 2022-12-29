import unittest

from operations.core import (
    remove_links_emojis, translate_text,
    geograpy_woi, get_capital_words
)

class testOperationsCore(unittest.TestCase):  
    @classmethod  
    def setUp(self):
        self.tweet1 = 'Κατεσβέσθη <a href="https://twitter.com/hashtag/πυρκαγιά">#πυρκαγιά</a> σε κεραμοσκεπή οικίας, στο δήμο Κατερίνης Πιερίας.'\
        '🚒🚒Επιχείρησαν 15 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με 5 οχήματα.'
        self.tweet2 = 'Σε εξέλιξη επιχείρηση ανάσυρσης ατόμου από αμαξοστοιχία τρένου στο Κρυονέρι Αττικής.'\
        '🚒🚒Επιχειρούν 6 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με 2 οχήματα.'\
        '<a href="https://t.co/5JSKRCC7Bt">https://t.co/5JSKRCC7Bt</a>'
        self.tweet3 = 'Ολοκληρώθηκε ο <a href="https://twitter.com/hashtag/απεγκλωβισμός">#απεγκλωβισμός</a> τραυματισμένου ατόμου  από Ε.Ι.Χ. αυτοκίνητο και παραδόθηκε στο ΕΚΑΒ, συνεπεία τροχαίου, στη Δ.Ε. Παλιανής (διαστάυρωση Άγιος Θωμάς) Ηρακλείου Κρήτης. Επιχείρησαν 9 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με 3 οχήματα.'
        self.free_text3 = 'Ολοκληρώθηκε ο απεγκλωβισμός τραυματισμένου ατόμου από Ε.Ι.Χ. αυτοκίνητο και παραδόθηκε στο ΕΚΑΒ, συνεπεία τροχαίου, στη Δ.Ε. Παλιανής διαστάυρωση Άγιος Θωμάς Ηρακλείου Κρήτης. Επιχείρησαν 9 πυροσβέστες με 3 οχήματα.'
        self.free_text1 = 'Κατεσβέσθη πυρκαγιά σε κεραμοσκεπή οικίας, στο δήμο Κατερίνης Πιερίας.'\
        'Επιχείρησαν 15 πυροσβέστες με 5 οχήματα.'
        self.freee_text2 = 'Σε εξέλιξη επιχείρηση ανάσυρσης ατόμου από αμαξοστοιχία τρένου στο Κρυονέρι Αττικής.'\
        'Επιχειρούν 6 πυροσβέστες με 2 οχήματα.'
        self.translated1 = 'Operation to rescue a person from a train in Kryoneri, Attica'
    
    def test_remove_links_emojis(self):
        self.maxDiff=None
        self.assertEqual(remove_links_emojis(self.tweet1), self.free_text1)
        self.assertEqual(remove_links_emojis(self.tweet2), self.freee_text2)
        print(remove_links_emojis(self.tweet3))
        self.assertEqual(remove_links_emojis(self.tweet3), self.free_text3)
        self.assertEqual(remove_links_emojis(""), "")

    # def test_translate_text(self):
    #     text = self.tweet2.split('.')[0]
    #     self.assertEqual(translate_text(text), self.translated1)

    # def test_geograpy_woi(self):
    #     self.assertEqual(geograpy_woi(self.translated1), 'Kryoneri')

    # def test_get_capital_words(self):
    #     self.assertEqual(get_capital_words(self.free_text1), 'Κατερίνης Πιερίας Επιχείρησαν')


if __name__ == '__main__':
    unittest.main()