const http = require('http');
const bodyParser = require('body-parser');
const Twit = require('twit');
const WebSocket = require('ws');
const express = require('express');
const fetch = require('node-fetch');

const T = new Twit({
  consumer_key:         process.env.CONSUMER_KEY,
  consumer_secret:      process.env.CONSUMER_SECRET,
  access_token:         process.env.ACCESS_TOKEN,
  access_token_secret:  process.env.ACCESS_SECRET,
  timeout_ms:           60*1000,
});

const app = express();
app.use(bodyParser.json());
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });


function broadcast(message) {
  wss.clients.forEach(function each(client) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

function hasProgram(program) {
  return program.statements.length > 0;
}

function handleProgramInput(programText, user) {
  return fetch('http://localhost:6789/parse', {
    method: 'POST',
    body: JSON.stringify({
      programText
    }),
    headers: {
      'Content-Type': 'application/json',
    }
  })
    .then(data => (Promise.all([data, data.json()])))
    .then(back => {
      const [response, data] = back;

      if (response.status === 200 && hasProgram(data.program)) {
        broadcast(JSON.stringify({
          user,
          program: data.program
        }));
        console.log('success!');
        return { success: true };
      } else {
        console.log('fail!');
        return { success: false };
      }
    });
}

const stream = T.stream('statuses/filter', { track: '#280canvas' });

stream.on('tweet', tweet => {
  handleProgramInput(tweet.text, {
    screenName: tweet.user.screen_name,
    name: tweet.user.name,
    profileImage: tweet.user.profile_image_url_https,
  })
    .then((response) => {
      if (!response.success) {
        console.log('No success!');
        T.post('statuses/update', { status: `@${tweet.user.screen_name} We couldn't compile your rend script! 😔` });
      }
    })
    .catch(error => {
      T.post('statuses/update', { status: `@${tweet.user.screen_name} We couldn't compile your rend script! 😔` });
    });
});

setInterval(() => broadcast('heartbeat'), 1000);


app.post('/draw', (req, res) => {
  handleProgramInput(req.body.programText, {
    screenName: 'cliUser',
    name: 'cli user',
    profileImage: null,
  })
    .then((response) => {
      if (response.success) {
        res.sendStatus(200);
      } else {
        res.sendStatus(400);
      }
    })
    .catch(() => res.sendStatus(400))
});

server.listen(5577, function listening() {
  console.log('Listening on %d', server.address().port);
});
