import unittest

from operations.core import (
    remove_links_emojis
)

class testOperationsCore(unittest.TestCase):  
    @classmethod  
    def setUp(self):
        self.tweet1 = 'Κατεσβέσθη <a href="https://twitter.com/hashtag/πυρκαγιά">#πυρκαγιά</a> σε κεραμοσκεπή οικίας, στο δήμο Κατερίνης Πιερίας.'\
        '🚒🚒Επιχείρησαν 15 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με 5 οχήματα.'
        self.tweet2 = 'Σε εξέλιξη επιχείρηση ανάσυρσης ατόμου από αμαξοστοιχία τρένου στο Κρυονέρι Αττικής.'\
        '🚒🚒Επιχειρούν 6 <a href="https://twitter.com/hashtag/πυροσβέστες">#πυροσβέστες</a> με 2 οχήματα.'\
        '<a href="https://t.co/5JSKRCC7Bt">https://t.co/5JSKRCC7Bt</a>'


    def test_remove_links_emojis(self):
        expected_text1 = 'Κατεσβέσθη πυρκαγιά σε κεραμοσκεπή οικίας, στο δήμο Κατερίνης Πιερίας.'\
        'Επιχείρησαν 15 πυροσβέστες με 5 οχήματα.'
        expected_text2 = 'Σε εξέλιξη επιχείρηση ανάσυρσης ατόμου από αμαξοστοιχία τρένου στο Κρυονέρι Αττικής.'\
        'Επιχειρούν 6 πυροσβέστες με 2 οχήματα.'
        self.assertEqual(expected_text1, remove_links_emojis(self.tweet1))
        self.assertEqual(expected_text2, remove_links_emojis(self.tweet2))


if __name__ == '__main__':
    unittest.main()