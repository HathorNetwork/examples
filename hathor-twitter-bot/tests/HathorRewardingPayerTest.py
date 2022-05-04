import unittest
from usecase import HathorRewardingPayer
from usecase import full_node_mainnet_url


class HathorRewardingPayerTest(unittest.TestCase):

    def test_valid_testnet_address(self):
        payer = HathorRewardingPayer()
        self.assertTrue(payer.is_valid_address('WdaaBTSs5tuh3qSZ4TMxL3sYUsdkh2EDku'))

    def test_invalid_testnet_address(self):
        payer = HathorRewardingPayer()
        self.assertFalse(payer.is_valid_address('WdaaBTSs5tuh3qSZ4TMxL3sYUsdkh2EDkF'))

    def test_valid_maintnet_address(self):
        payer = HathorRewardingPayer(full_node_mainnet_url)
        self.assertTrue(payer.is_valid_address('HKrn2NVRqzo7oNhQdu5T4b3PxFS1h8uE1m'))

    def test_invalid_maintnet_address(self):
        payer = HathorRewardingPayer(full_node_mainnet_url)
        self.assertFalse(payer.is_valid_address('HKrn2NVRqzo7oNhQdu5T4b3PxFS1h8uE1F'))


if __name__ == '__main__':
    unittest.main()
