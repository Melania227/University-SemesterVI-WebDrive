const mongoose = require('mongoose');
const FolderSchema = require('./Folder.js').model('Folder').schema

const DriveSchema = mongoose.Schema({
    user: {
        type: String,
        required: true
    },
    maxBytes: {
        type: Number,
        required: true
    },
    currentBytes: {
        type: Number,
        required: true
    },
    root: {
        type: FolderSchema,
        required: true        
    },
    shared:{
        type: [[String]],
        require: true
    }
});

module.exports = mongoose.model('Drive', DriveSchema);