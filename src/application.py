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
#
# client = PeonyClient(consumer_key=CONSUMER_KEY,
#                      consumer_secret=CONSUMER_SECRET,
#                      access_token=ACCESS_TOKEN,
#                      access_token_secret=ACCESS_SECRET,
#                      )
#
# req = client.stream.statuses.filter.post(track=TRACKING_STRING)

client = []

async def stream():
    # # req is an asynchronous context
    # async with req as stream:
    #     # stream is an asynchronous iterator
    #     async for tweet in stream:
    #         # check that you actually receive a tweet
    #         if peony.events.tweet(tweet):
    #             # you can then access items as you would do with a
    #             # `PeonyResponse` object
    #             user_id = tweet['user']['id']
    #             username = tweet.user.screen_name
    #
    #             msg = json.dumps({
    #                 'username': username,
    #                 'program': reece_parse(tweet.text)
    #             })
    #             for ws in client:
    #                 await ws.send(msg)
    while True:
        await asyncio.sleep(1.0)
        print('broadcasting!')
        for ws in client:
            try:
                await ws.send('hello there!')
            except websockets.ConnectionClosed:
                pass

async def time(websocket, path):
    print('client connected')

    client.append(websocket)
#    await websocket.send(message)

start_server = websockets.serve(time, '127.0.0.1', os.environ.get('PORT', 5577))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.async(stream())
asyncio.get_event_loop().run_forever()
