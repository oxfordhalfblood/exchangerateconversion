import unittest
import rateconversion

class Testrateconverse(unittest.TestCase):
    
    
    def test_apiextract(self):
        current = "https://api.ratesapi.io/api/latest"
        historic = "https://api.ratesapi.io/api/"

        msg1 = {'action': 'getCurrent', 'context': {'base': 'AUD', 'symbols': ['USD', 'GBP']}}
        msg2 = {'action': 'getcurrent', 'created_at': 1568041517, 'context': {'base': 'AFRI', 'symbols': ['USD', 'GBP']}}
        msg3 = {'action': 'getlinf', 'created_at': 1568041517, 'context': {'base': 'AUD', 'symbols': ''}}
        msg4 = {'action': 'getCurrent', 'created_at': 1568041517, 'context': {'base': 'AUD', 'symbols': 0}}
        msg5={'action': 'historicData', 'created_at': 1568041517, 'context': {'base': 'AUD', 'symbols': ['HKD', 'CZK', 'NOK', 'CAD'], 'date': '1999-06-06'}}
        # self.assertEqual(rateconversion.apiextract(current,msg1), 200)
        # self.assertEqual(rateconversion.apiextract(historic,msg5), 200)
        self.assertFalse(rateconversion.apiextract(current,msg2))
        self.assertTrue(rateconversion.apiextract(current,msg1))
        self.assertTrue(rateconversion.apiextract(current,msg3))


if __name__ == '__main__':
    unittest.main()