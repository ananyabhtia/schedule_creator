/*jshint strict:false */
/* jshint node: true */
/*jshint esversion: 8 */
/*global console*/

const express = require('express');
const app = express();
const port = 3000;
const times = require('./assets/json/times.json');

app.use(express.static('./'));

app.get(function (req, res) {
  res.render('index.html');
});

app.get("/log-in", function (req, res) {
    res.render('log-in.html');
});

app.get("/create-account", function (req, res) {
    res.render('create-account.html');
});

app.get("/create-schedule", function (req, res) {
    res.render('create-schedule.html');
});

app.get('/times-data', (req, res) => {
    res.json(times);
  });

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
  })