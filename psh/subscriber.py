import argparse
import asyncio

import zmq
import zmq.asyncio


class Subscriber(object):

    def __init__(self, endpoint, topics, count=20):
        self.endpoint = endpoint
        self.topics = topics
        self.count = count
        self.ctx = zmq.asyncio.Context.instance()
        self.socket = self.ctx.socket(zmq.SUB)

    async def run(self):
        self.socket.connect(self.endpoint)
        for topic in self.topics:
            print(f"Subscriber: subscribing to '{topic}'")
            self.socket.subscribe(topic.encode())
            await self.recv()  # check for LVC publication
            await asyncio.sleep(3)  # simulate a late subscriber

        for _ in range(self.count):
            await self.recv()

        for topic in self.topics:
            print(f"Subscriber: un-subscribing from '{topic}'")
            self.socket.unsubscribe(topic)

    async def recv(self, timeout=1):
        try:
            topic, message = await asyncio.wait_for(
                self.socket.recv_multipart(), timeout=timeout)
            print(f"Subscriber: Received {topic}: {message}")
        except asyncio.TimeoutError:
            pass
