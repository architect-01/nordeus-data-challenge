const { Client } = require('pg');
const path = require('path');
const express = require('express')
const cors = require('cors')

require('dotenv').config()

const app = express()

app.use(cors())


const port =  process.env.PORT || 3001;
const DATABASE_URL = process.env.DATABASE_URL

app.use(express.static(path.join(__dirname, 'client/build')));

console.log(DATABASE_URL)

const client = new Client({
  connectionString: DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

client.connect();

app.get('/api/scoreboard', (req, resp) => {
  let {league_id} = req.query;

  client.query(`SELECT * FROM scoreboards WHERE league_id = ${league_id} ORDER BY points DESC, goal_diff DESC, team_name ASC;`, (err, res) => {
    if (err) resp.json({'error': `You need to pass 'league_id' query param of type INT - You passed '${league_id}'`})
    else resp.json(res.rows)
  });
})

app.get('*', (req, resp) => {
  resp.sendFile(path.join(__dirname, 'client', 'build', 'index.html'));
})

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`)
})