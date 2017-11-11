import asyncio
import http
import json
import os
import websockets
import peony
from peony import PeonyClient

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
TRACKING_STRING = '#280canvas'


def reece_parse(message):
    return message

client = PeonyClient(consumer_key=CONSUMER_KEY,
                     consumer_secret=CONSUMER_SECRET,
                     access_token=ACCESS_TOKEN,
                     access_token_secret=ACCESS_SECRET,
                     )

req = client.stream.statuses.filter.post(track=TRACKING_STRING)


class HttpWSSProtocol(websockets.WebSocketServerProtocol):
    async def process_request(self, path, request_headers):
        if path == '/':
            return http.HTTPStatus(http.HTTPStatus.OK)


async def time(websocket, path):
    print('websocketing')

    # req is an asynchronous context
    async with req as stream:
        # stream is an asynchronous iterator
        async for tweet in stream:
            # check that you actually receive a tweet
            if peony.events.tweet(tweet):
                # you can then access items as you would do with a
                # `PeonyResponse` object
                user_id = tweet['user']['id']
                username = tweet.user.screen_name

                msg = json.dumps({
                    'username': username,
                    'program': reece_parse(tweet.text)
                })
                await websocket.send(msg)

start_server = websockets.serve(time, '127.0.0.1', os.environ.get('PORT', 5577), klass=HttpWSSProtocol)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
