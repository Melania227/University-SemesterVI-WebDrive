const mongoose = require('mongoose');

const FileSchema = mongoose.Schema({
    type: {
        type: String,
        required: true
    },
    name: {
        type: String,
        required: true
    },
    extension: {
        type: String,
        required: true
    },
    size: {
        type: Number,
        required: true
    },
    data: {
        type: String,
        required: true
    }
});

module.exports = mongoose.model('File', FileSchema);