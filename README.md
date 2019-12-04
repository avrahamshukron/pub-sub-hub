# PubSubHub
An example of using the Pub/Sub pattern with LVC through central hub using 0MQ

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
To test 