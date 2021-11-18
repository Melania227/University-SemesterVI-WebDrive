const mongoose = require('mongoose');


const FolderSchema = mongoose.Schema({
    type: {
        type: String,
        required: true
    },
    directories: {
        type: [mongoose.Schema.Types.Mixed],
        required: true
    }
});

module.exports = mongoose.model('Folder', FolderSchema);