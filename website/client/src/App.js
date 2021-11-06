import React, { useState } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import axios from "axios";
import './App.css';

async function request_league_scb(league_id, set_scoreboard_data) {

  axios.get(`https://nordeus-data-challenge.herokuapp.com/api/scoreboard?league_id=${league_id}`)
  .then(function (response) {
    // handle success
    console.log(response.data)
    set_scoreboard_data(response.data)

  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .then(function () {
    // always executed
  });


}

function App() {
  const [league_id, set_league_id] = useState(undefined);
  const [scoreboard_data, set_scoreboard_data] = useState([]);

  return (
    <div className="App">
      <header className="App-header">
        <div className = "VerticalSplit">

          <div className = "VComp">
            <img src="nordeus_logo.png" className="App-logo" alt="logo" />
            <p>
              Solution for Nordeus Data Challenge.
            </p>
            Challenge information and solution's source code available at github : <br/>
            <a
              className="App-link"
              href="https://github.com/architect-01/nordeus-data-challenge"
              target="_blank"
              rel="noopener noreferrer"
            >
              architect-01/nordeus-data-challenge
            </a>
          </div>

          <div className = "VComp ApiFrontend">
      
            <FormControl className = 'SelectForm'>
              <InputLabel id="demo-simple-select-label">Select League</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={league_id}
                label="LeagueId"
                onChange={(e) => { set_league_id(e.target.value); request_league_scb(e.target.value, set_scoreboard_data)}}
              >
                {[1,2,3,4,5,6,7,8].map((l_id, idx) => (<MenuItem value={l_id}>{l_id}</MenuItem>)) }
              </Select>
            </FormControl>
    
            <hr/>

            {(league_id != undefined) ? (
              <TableContainer component={Paper}>
                <Table sx={{ minWidth: 550 }} aria-label="simple table">
                  <TableHead>
                    <TableRow>
                      <TableCell>Rank</TableCell>
                      <TableCell align="right">Club</TableCell>
                      <TableCell align="right">Points</TableCell>
                      <TableCell align="right">Goal Difference</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {scoreboard_data.map((row, idx) => (
                      <TableRow
                        key={row.name}
                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                      >
                        <TableCell component="th" scope="row">{idx+1}</TableCell>
                        <TableCell align="right">{row.team_name}</TableCell>
                        <TableCell align="right">{row.points}</TableCell>
                        <TableCell align="right">{row.goal_diff}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer> ) : <p>Once the league id is selected here will the Scoreboard be presented.</p> }

            </div>
          </div>
      </header>
    </div>
  );
}

export default App;

