import re
import requests
import json
from tweepy import StreamingClient
from tweepy import StreamRule
from urllib import parse

# Twitter Credentials
bearer_token: str = ''

# Hathor Rewarding
address_pattern = r'HTR\[(\w+)\]'
hashtags = ['#BlockchainMadeEasy', '#BuildOnHathor']
htr_reward = 1

# Wallet Headless
wallet_id = 'twitter-wallet'
wallet_seed_key = 'default'
wallet_base_url = 'http://localhost:8000'
wallet_data = {
    'wallet-id': wallet_id,
    'seedKey': wallet_seed_key
}
wallet_headers = {
    'x-wallet-id': wallet_id
}
wallet_ready_status = 3

# Full Node
full_node_mainnet_url = 'https://node1.mainnet.hathor.network'
full_node_testnet_url = 'https://node1.testnet.hathor.network'


class HathorRewardingPayer:

    def __init__(self, full_node=full_node_testnet_url):
        self.full_node_base_url = full_node
        while not self.is_wallet_ready():
            self.start_wallet()

    def response_to_json(self, response):
        return json.loads(json.dumps(response.json()))

    def is_wallet_ready(self):
        url = parse.urljoin(wallet_base_url, '/wallet/status')
        response = requests.get(url, headers=wallet_headers)
        jsonResponse = self.response_to_json(response)
        if "success" in jsonResponse:
            connected_status = self.response_to_json(response)["success"]
        else:
            connected_status = self.response_to_json(response)["statusCode"] == wallet_ready_status

        return connected_status

    def start_wallet(self):
        url = parse.urljoin(wallet_base_url, '/start')
        response = requests.post(url, data=wallet_data)
        print('Connection to Wallet Headless:')
        print(response.json())

    def is_valid_address(self, address):
        url = parse.urljoin(self.full_node_base_url, '/v1a/validate_address/' + address)
        response = requests.get(url, headers=wallet_headers)
        return self.response_to_json(response)["valid"]

    def pay_tweet(self, address):

        if self.is_valid_address(address):

            url = parse.urljoin(wallet_base_url, '/wallet/simple-send-tx')
            data = {
                'address': address,
                'value': htr_reward
            }
            response = requests.post(url, json=data, headers=wallet_headers)
            print('Rewarding Transaction:')
            print(response.json())
        else:
            print("Invalid Address! No reward will be paid.")


class HathorStreamingClient(StreamingClient):

    def __init__(self, twitter_token, full_node=full_node_testnet_url):
        super(HathorStreamingClient, self).__init__(twitter_token)
        for hashtag in hashtags:
            self.add_rules(StreamRule(hashtag))
        self.payer = HathorRewardingPayer(full_node)

    def on_connect(self):
        print('Connection to Twitter has been established!')

    def on_tweet(self, tweet):
        print('New tweet!')
        address = re.search(address_pattern, tweet.text)
        self.payer.pay_tweet(address.group(1))

    def on_disconnect(self):
        print('Connection to Twitter has been closed!')