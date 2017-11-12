const Twit = require('twit');
const WebSocket = require('ws');

const T = new Twit({
  consumer_key:         process.env.CONSUMER_KEY,
  consumer_secret:      process.env.CONSUMER_SECRET,
  access_token:         process.env.ACCESS_TOKEN,
  access_token_secret:  process.env.ACCESS_SECRET,
  timeout_ms:           60*1000,
});

const wss = new WebSocket.Server({ port: 5577 });


function broadcast(message) {
  wss.clients.forEach(function each(client) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

const stream = T.stream('statuses/filter', { track: '#280canvas' });

stream.on('tweet', tweet => {
  // fetch parsed program
  // then
  broadcast(JSON.stringify(tweet))
});

