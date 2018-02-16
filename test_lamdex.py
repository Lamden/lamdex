from unittest import TestCase
import lamdex
import requests
import mock

class Test_Lamdex(TestCase):
    def test_return_rate_returns_1(self):
        self.assertEqual(lamdex.return_rate('EOS', test=True), 1)

    def test_return_rate_fails_in_non_supported_tokens(self):
        try:
            lamdex.return_rate('XXX')
            self.assertTrue(False)
        except Exception as e:
            print(e)
            self.assertTrue(True)

    def test_return_rate_is_accurate(self):
        url = 'https://api.hitbtc.com/api/2/public/ticker/TAUBTC'
        r = requests.get(url)
        last = float(r.json()['last'])
        self.assertEqual(lamdex.return_rate('TAU'), last)

    def test_forex_test_returns_1(self):
        self.assertEqual(lamdex.forex('TAU', 'EOS', test=True), 1)

    def test_forex_is_accurate(self):
        url = 'https://api.hitbtc.com/api/2/public/ticker/TAUBTC'
        r = requests.get(url)
        last_tau = float(r.json()['last'])

        url = 'https://api.hitbtc.com/api/2/public/ticker/EOSBTC'
        r = requests.get(url)
        last_eos = float(r.json()['last'])
        test_forex = last_tau/last_eos

        self.assertEqual(lamdex.forex('TAU', 'EOS'), test_forex)
