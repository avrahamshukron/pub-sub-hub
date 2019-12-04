from random import shuffle

import zmq
import asyncio
from itertools import product


class Publisher(object):
    messages = ["what?", "no way!", "hell yeah!", "42"]

    def __init__(self, topics, endpoint):
        self.topics = topics
        self.endpoint = endpoint
        self.ctx = zmq.Context.instance()
        self.sock = self.ctx.socket(zmq.PUB)

    async def run(self):
        self.sock.connect(self.endpoint)
        publications = list(product(self.topics, self.messages))
        shuffle(publications)
        for topic, message in publications:
            print(f"Publisher: publishing: [{topic}] - {message}")
            self.sock.send_multipart((topic.encode(), message.encode()))
            await asyncio.sleep(1)
