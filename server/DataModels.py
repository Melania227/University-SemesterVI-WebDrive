#Models

def newDrive(maxBytes):
    drive = {
        "maxBytes": maxBytes,
        "currentBytes": 0,
        "root": newFolder("root"),
        "shared": newFolder("shared")
    }
    return drive

def newFolder(name):
    folder = {
        "type": "folder",
        "name": name,
        "directories": [],
        "size" : 0

    }
    return folder

def newFile(name, data, size, dateTime):
    file = {
        "type": "file",
        "name" : name,
        "data" :  data,
        "size" : size,
        "creationDate": dateTime,
        "modificationDate": dateTime
    }
    return file