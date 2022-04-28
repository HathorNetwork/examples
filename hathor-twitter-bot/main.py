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
wallet_ready_status = 'Ready'

# Full Node
full_node_base_url = 'https://node1.testnet.hathor.network/v1a'


class HathorRewardingPayer:

    def __init__(self):
        while not self.is_wallet_ready():
            self.start_wallet()

    def is_wallet_ready(self):
        url = parse.urljoin(wallet_base_url, '/wallet/status')
        response = requests.get(url, headers=wallet_headers).json()
        response = str(response).replace("\'", "\"")
        print(response)
        response = {"success": False, "message": "Invalid wallet id parameter.", "statusMessage": ""}
        response = json.dumps(response)
        status = json.loads(response)["message"]
        print(status)
        return status == wallet_ready_status

    def start_wallet(self):
        url = parse.urljoin(wallet_base_url, '/start')
        response = requests.post(url, data=wallet_data)
        print('Connection to Wallet Headless:')
        print(response.json())

    def is_valid_address(self, address):
        url = parse.urljoin(full_node_base_url, '/validate_address/' + address)
        response = requests.get(url, headers=wallet_headers)
        jsonResponse = json.loads(response.json())
        return jsonResponse.get('valid')

    def pay_tweet(self, address):
        url = parse.urljoin(wallet_base_url, '/wallet/simple-send-tx')
        data = {
            'address': address,
            'value': htr_reward
        }
        response = requests.post(url, json=data, headers=wallet_headers)
        print('Rewarding Transaction:')
        print(response.json())


class HathorStreamingClient(StreamingClient):

    def __init__(self, twitter_token):
        super(HathorStreamingClient, self).__init__(twitter_token)
        for hashtag in hashtags:
            self.add_rules(StreamRule(hashtag))
        self.payer = HathorRewardingPayer()

    def on_connect(self):
        print('Connection to Twitter has been established!')

    def on_tweet(self, tweet):
        print('New tweet!')
        address = re.search(address_pattern, tweet.text)
        self.payer.pay_tweet(address.group(1))

    def on_disconnect(self):
        print('Connection to Twitter has been closed!')


if __name__ == '__main__':

    streaming = HathorStreamingClient(twitter_token=bearer_token)

    try:
        streaming.filter()
    except KeyboardInterrupt:
        pass
    finally:
        streaming.disconnect()
