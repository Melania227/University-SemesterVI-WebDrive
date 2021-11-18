const { response } = require('express');
const express = require('express');
const { remove } = require('../models/Drive');
const router = express.Router();
const Drive = require('../models/Drive')
const Folder = require('../models/Folder')
const File = require('../models/File')

//GET 
router.get('/', async(req, res) => {
    try {
        const drive = await Drive.find();
        res.json(drive);
    } catch (error) {
        res.status(401).send('Ha ocurrido un error.');
    }
});

//GET list
router.get('/list', async(req, res) => {
    try {
        const drive = await Drive.find();
        resultado = []
        drive.forEach(element => {
            resultado.push(element.user);
        });


        res.json(resultado);
    } catch (error) {
        res.status(401).send('Ha ocurrido un error.');
    }

});

//GET drive
router.get('/:user', async(req, res) => {
    try {
        const drive = await Drive.findOne({ user: req.params.user });
        console.log(drive);
        res.json(drive);
    } catch (error) {
        res.status(401).send('Ha ocurrido un error.');
    }

});

//POST
//E: {user,maxBytes}
router.post('/', async(req, res) => {

    try {

        const drive = new Drive({
            user: req.body.user,
            maxBytes: req.body.maxBytes,
            currentBytes: 0,
            root: new Folder({
                type: "folder",
                directories: []
            }),
            shared: []
        });

        console.log(drive);

        await drive.save(function(err) {
            if (err) {
                res.status(401).send('Ha ocurrido un error.1');
            } else {
                saveDrive = drive.toObject();
                res.json(drive);
            }
        }); //metodo de mongoose para guardar 

    } catch {
        res.status(401).send('Ha ocurrido un error.2');
    }

});

//PATCH
//E: {drive}
router.patch('/', async(req, res) => {
    try {
        let conditions = {user: req.body.drive.user};
        const updateDrive = await Drive.updateOne(conditions, req.body.drive);
        res.json(updateDrive);
    } catch {
        res.status(401).send('Ha ocurrido un error.2');
    }

});

module.exports = router;