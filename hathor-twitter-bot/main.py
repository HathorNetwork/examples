import re
import requests
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

# Full Node
full_node_base_url = 'https://node1.testnet.hathor.network/v1a'


class HathorRewardingPayer:

    def __init__(self):
        self.start_wallet()

    def start_wallet(self):
        
        url = parse.urljoin(wallet_base_url, '/start')
        data = {
            'wallet-id': wallet_id,
            'seedKey': wallet_seed_key
        }
        response = requests.post(url, data=data)
        print('Connection to Wallet Headless:')
        print(response.json())

    def validate_address(self, address):

        url = parse.urljoin(full_node_base_url, '/validate_address/' + address)

        headers = {
            'x-wallet-id': wallet_id
        }
        response = requests.get(url, headers=headers)

    def pay_tweet(self, address):

        url = parse.urljoin(wallet_base_url, '/wallet/simple-send-tx')
        headers = {
            'x-wallet-id': wallet_id
        }
        data = {
            'address': address,
            'value': htr_reward
        }

        response = requests.post(url, json=data, headers=headers)
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
