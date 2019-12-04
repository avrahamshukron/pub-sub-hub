
import argparse
import asyncio

import zmq
import zmq.asyncio

ACTION_SUBSCRIBE = b"\x01"


class PubSubHub(object):

    def __init__(self, subscription_endpoint, publication_endpoint):
        self.subscription_endpoint = subscription_endpoint
        self.publication_endpoint = publication_endpoint
        self.cache = {}
        self.subscribers = 0
        self.done = False
        self.ctx = zmq.asyncio.Context.instance()
        self.xpub = self.ctx.socket(zmq.XPUB)
        self.xsub = self.ctx.socket(zmq.XSUB)

    async def wait_for_subscriptions(self):
        print(f"Hub: listening for subscribers on {self.subscription_endpoint}")
        while not self.done:
            await self.handle_single_subscription()
        print("Hub: all subscribers are now gone")

    async def bind(self):
        self.xpub.bind(self.subscription_endpoint)
        self.xsub.bind(self.publication_endpoint)

    async def handle_single_subscription(self):
        msg = await self.xpub.recv()
        action = msg[:1]
        topic = msg[1:]
        action_name = "subscribed" if action == ACTION_SUBSCRIBE else "unsubscribed"
        self.subscribers += 1 if action == ACTION_SUBSCRIBE else -1
        self.done = self.subscribers == 0
        print(f"Hub: someone {action_name} on {topic}")
        if action == ACTION_SUBSCRIBE and topic in self.cache:
            print(f"Hub: LVC hit for '{topic}'. Re-publishing")
            await self.xpub.send_multipart((topic, self.cache.get(topic)))

    async def wait_for_publications(self):
        await self.xsub.send(ACTION_SUBSCRIBE)  # subscribe to all topics
        print(f"Hub: listening for publishers on {self.publication_endpoint}")
        try:
            while True:
                await asyncio.wait_for(
                    self.handle_singe_publication(), timeout=10)
        except asyncio.TimeoutError:
            print("Hub: no more publication")

    async def handle_singe_publication(self):
        topic, msg = await self.xsub.recv_multipart()
        print(f"Hub: forwarding: {topic} - {msg}")
        self.cache[topic] = msg
        await self.xpub.send_multipart((topic, msg))

    async def run(self):
        await self.bind()
        await asyncio.gather(
            self.wait_for_subscriptions(),
            self.wait_for_publications()
        )
