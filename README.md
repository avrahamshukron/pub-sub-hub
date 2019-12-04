# PubSubHub
An example of using the Pub/Sub pattern with LVC through central hub using 0MQ
It is written in Python3 using `asyncio`.

The project is basically an experiment with `0MQ` and `asyncio`.

Status: [![CircleCI](https://circleci.com/gh/avrahamshukron/pub-sub-hub/tree/master.svg?style=svg)](https://circleci.com/gh/avrahamshukron/pub-sub-hub/tree/master)

```text
+-----------+    +-----------+   +-----------+
| Publisher |    | Publisher |   | Publisher |
+-----------+\   +-----------+  /+-----------+
              \        |       /
               \       |      /
               \/     \|/    \/
                 +-----------+
                 |    Hub    |
                 +-----------+
                /      |      \
               /       |       \
              /        |        \
             \/       \|/       \/
+------------+   +------------+  +------------+
| Subscriber |   | Subscriber |  | Subscriber |
+------------+   +------------+  +------------+
```

### The Hub
The hub is a process that has two endpoints:
1. XPUB socket, to receive incoming subscriptions from subscribers.
2. XSUB socket, to receive incoming publications from publishers.

#### Last-value Caching
The hub also maintains a cache with the last publication on each topic.
When a subscriber subscribes to a topic, if the cache has an entry for that
topic it will then re-publish that entry so that the new subscriber will have
the latest data. Real-world implementation should provide some mechanism to
control this behavior as it is not appropriate to cache every message (E.g a
temporal event which is only relevant to the time it was published) 

## See it in action
```shell script
# In the repo top directory:
python3 -m venv .psh-env
. .psh-env/bin/activate
pip install -r requirements.txt

python3 psh/main.py
```
The `main.py` script creates the Hub, a subscriber and a publisher, and run
them all together in the same process using dummy data.