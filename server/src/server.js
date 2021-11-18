const express = require('express');
const app = express();
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv/config');

// Middleware
app.use(cors());

app.use(
    express.urlencoded({
        extended: true
    })
);
app.use(express.json());

// imports ROUTES

const drivesRoute = require('./routes/drives');

app.use('/drives', drivesRoute);

mongoose.connect(
    process.env.DB_CONNECTION, {
        useUnifiedTopology: true,
        useNewUrlParser: true
    },
    () => {
        console.log('connected to WebDrive DB!!!');
    }
);

// server listing in  port 3000
app.listen(3000);