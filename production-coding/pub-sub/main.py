from typing import Dict, Set
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    key: int
    title: str
    payload: str
    timestamp: float

class Subscriber:
    def __init__(self, name: str):
        self.name = name

    def handle(self, message: Message):
        print(f"Receieved message : {message.title}")

class PubSubSystem:
    def __init__(self):
        self.subscribers: Dict[str, Set[Subscriber]] = {}

    def subscribe(self, topic: str, subscriber: Subscriber):
        if topic not in self.subscribers:
            self.subscribers[topic] = set()

        self.subscribers[topic].add(subscriber)

    def unsubscribe(self, topic: str, subscriber: Subscriber):
        if topic not in self.subscribers:
            raise KeyError(f"Subscriber {subscriber.name} not subscribed to topic {topic}")

        self.subscribers[topic].remove(subscriber)

        if len(self.subscribers[topic]) == 0:
            self.subscribers.pop(topic)

    def publish(self, topic: str, message: Message):
        subs = self.subscribers.get(topic, set())

        for subscriber in subs:
            print(f"Delivering message {message.title} to subscriber {subscriber.name}")
            subscriber.handle(message)

class Driver:
    @staticmethod
    def main():
        system = PubSubSystem()

        subscriber1 = Subscriber("sub1")
        subscriber2 = Subscriber("sub2")
        subscriber3 = Subscriber("sub3")

        system.subscribe("topic1", subscriber1)
        system.subscribe("topic1", subscriber2)

        system.publish("topic1", Message(1, "Hello", "Sample payload", datetime.now()))
