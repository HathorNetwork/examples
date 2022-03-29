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
