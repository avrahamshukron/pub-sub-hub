from psh.hub import PubSubHub
from psh.subscriber import Subscriber
from psh.publisher import Publisher

import asyncio

PUBLICATION_ENDPOINT = "tcp://0.0.0.0:6666"
SUBSCRIPTION_ENDPOINT = "tcp://0.0.0.0:5555"

topics = ["pub/foo", "pub/bar", "pub/foo/bak", "pub/bar/baz"]


async def main():
    hub = PubSubHub(
        subscription_endpoint=SUBSCRIPTION_ENDPOINT,
        publication_endpoint=PUBLICATION_ENDPOINT)
    subscriber = Subscriber(SUBSCRIPTION_ENDPOINT, topics)
    publisher = Publisher(topics, PUBLICATION_ENDPOINT)
    await asyncio.gather(hub.run(), subscriber.run(), publisher.run())


if __name__ == '__main__':
    asyncio.run(main())
