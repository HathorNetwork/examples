from usecase import HathorStreamingClient
from usecase import bearer_token

if __name__ == '__main__':

    streaming = HathorStreamingClient(twitter_token=bearer_token)

    try:
        streaming.filter()
    except KeyboardInterrupt:
        pass
    finally:
        streaming.disconnect()
