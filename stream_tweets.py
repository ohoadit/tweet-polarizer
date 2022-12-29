from datetime import datetime
import json
import sys
import tweepy
from afinn import Afinn
from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf)

afinn = Afinn()

topic = 'tweet-polarizer'

search_term = "elon musk"

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


class MyStreamListener(tweepy.StreamingClient):

    def on_data(self, raw_data):
        tweet_data = json.loads(raw_data)
        tweet = tweet_data['data']
        id = tweet['id']
        text = tweet['text']
        payload = { 'id': id, 'text': text }
        score = afinn.score(tweet['text'])
        payload['sentiment'] = 'Positive' if score > 0 else 'Negative' if score < 0 else 'Neutral'
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y, %H:%M:%S")
        payload['timestamp'] = timestamp
        json_data = json.dumps(payload)
        producer.produce(topic, key="tweet", value=json_data, callback=acked)
        producer.poll(1)

    def on_request_error(self, status_code):
        print(f"Error occurred with status: {status_code}")
        sys.exit(1)


def get_streaming_client():
    return MyStreamListener(bearer_token='YOUR_BEARER_TOKEN_GOES_HERE')


if __name__ == "__main__":
    client = get_streaming_client()
    client.add_rules(tweepy.StreamRule(search_term))
    client.filter()