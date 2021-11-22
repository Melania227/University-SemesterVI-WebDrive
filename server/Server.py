from os import abort
from flask import Flask, request, Response, sessions, jsonify
from FileSystem import FileSystem

app = Flask(__name__)
fileSystem = FileSystem()


#Session Routes
@app.route('/users', methods =['POST'])
def postUser():
    user = request.json.get("user")
    maxBytes = request.json.get("maxBytes")
    return fileSystem.signUp(user, maxBytes)

@app.route('/users', methods =['GET'])
def getUsersList():
    user = request.json.get("user")
    return {"sesions":fileSystem.sessions, "drives":fileSystem.drives}

@app.route('/users/paths', methods =['GET'])
def getUsersPaths():
    user = request.json.get("user")
    return fileSystem.getCurrentPaths(user)
    

@app.route('/users/logIn', methods =['POST'])
def postLogIn():
    user = request.json.get("user")
    return fileSystem.logIn(user)


@app.route('/users/logOut', methods =['POST'])
def postLogout():
    user = request.json.get("user")
    return fileSystem.logOut(user)

@app.route('/users/cleanPaths', methods =['POST'])
def postLogout():
    user = request.json.get("user")
    return fileSystem.cleanPaths(user)

@app.route('/users/storage', methods =['GET'])
def postLogout():
    user = request.json.get("user")
    return fileSystem.getCurrentStorage(user)

#FileSystem Routes

#Folders Routes 
@app.route('/folders/current', methods =['GET'])
def getCurrentFolder():
    user = request.json.get("user")
    return fileSystem.getCurrentFolder(user)

@app.route('/folders', methods =['POST'])
def postFolder():
    user = request.json.get("user")
    name = request.json.get("name")
    return fileSystem.createFolder(user, name)

@app.route('/folders', methods =['DELETE'])
def deleteFolder():
    user = request.json.get("user")
    name = request.json.get("name")
    return fileSystem.delete(user, name)

@app.route('/folders', methods =['PATCH'])
def updateFolder():
    user = request.json.get("user")
    name = request.json.get("name")
    newName = request.json.get("newName")
    return fileSystem.updateFolder(user, name, newName)

@app.route('/folders/open', methods =['POST'])
def postOpenFolder():
    user = request.json.get("user")
    name = request.json.get("name")
    return fileSystem.openFolder(user, name)

@app.route('/folders/close', methods =['POST'])
def postCloseFolder():
    user = request.json.get("user")
    return fileSystem.closeFolder(user)

#Files Routes
@app.route('/files', methods =['POST'])
def postFile():
    user = request.json.get("user")
    name = request.json.get("name")
    data = request.json.get("data")
    return fileSystem.creatFile(user, name, data)

@app.route('/files', methods =['GET'])
def getFile():
    user = request.json.get("user")
    name = request.json.get("name")
    return fileSystem.openFile(user, name)

@app.route('/files', methods =['DELETE'])
def deleteFile():
    user = request.json.get("user")
    name = request.json.get("name")
    return fileSystem.delete(user, name)

@app.route('/files', methods =['PATCH'])
def updateFile():
    user = request.json.get("user")
    name = request.json.get("name")
    newName = request.json.get("newName")
    data = request.json.get("data")
    newData = request.json.get("newData")
    return fileSystem.updateFile(user, name, newName, newData)


#Main
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug = True)