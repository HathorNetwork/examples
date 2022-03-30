# Hathor Use Cases Samples
Repository with samples of use cases that integrate with the Hathor Network.

## Twitter Bot
Use case that implements a bot that fetches tweets containing previously defined hashtags related to Hathor. 
As soon as the bot detects a tweet with any of these hashtags, it rewards the user with some HTR. 

To receive the reward, the tweet must also contain the blockchain address to be used to send the HTR. 
The reward will be paid to only one address, i.e. if there are multiple addresses in the tweet, only the first address 
will be considered.

- **Hashtags**: #BlockchainMadeEasy, #BuildOnHathor
- **HTR Reward**: 0.01

### How to run?

Firstly, run the headless wallet locally:
- Clone the [project](https://github.com/HathorNetwork/hathor-wallet-headless) 
- Copy the `config.js` template to `src/config.js` and set the 24-words seed
- Execute `npm start`

More details on how to run the headless wallet are available in the [Headless Wallet Guide](https://hathor.gitbook.io/hathor/guides/wallet-headless/running-wallet-service)

Next, install the [Tweepy](https://github.com/tweepy/tweepy) package by running `pip install tweepy`

Finally, set your Twitter bearer token to the `bearer_token` variable of the `main.py` file and run the bot 
with the `python main.py` command. 

More details on how to get a Twitter bearer token from a developer account can be found
in the [Twitter API Credentials](#) section of the [Twitter Bot Guide](#).


