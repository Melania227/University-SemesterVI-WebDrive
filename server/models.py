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
        "directories": []
    }
    return folder

def newFile(name, data, extension):
    folder = {
        "type": "file",
        "name" : name,
        "extension": extension,
        "data" :  data   
    }
    return folder
