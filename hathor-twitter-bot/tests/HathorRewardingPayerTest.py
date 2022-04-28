import unittest
from main import HathorRewardingPayer

payer = HathorRewardingPayer()


class HathorRewardingPayerTest(unittest.TestCase):

    def test_valid_addres(self):
        self.assertTrue(payer.is_valid_address('WdaaBTSs5tuh3qSZ4TMxL3sYUsdkh2EDku'))


if __name__ == '__main__':
    unittest.main()
