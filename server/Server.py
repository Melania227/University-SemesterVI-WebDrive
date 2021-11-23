from os import abort
from flask import Flask, request, Response, sessions, jsonify
from flask_cors import cross_origin
from FileSystem import FileSystem

app = Flask(__name__)
fileSystem = FileSystem()


#Session Routes
@app.route('/users', methods =['POST'])
@cross_origin()
def postUser():
    user = request.json.get("user")
    maxBytes = request.json.get("maxBytes")
    return fileSystem.signUp(user, maxBytes)

@app.route('/users', methods =['GET'])
@cross_origin()
def getUsersList():
    user = request.json.get("user")
    return {"sesions":fileSystem.sessions, "drives":fileSystem.drives}

@app.route('/users/paths', methods =['GET'])
@cross_origin()
def getUsersPaths():
    user = request.json.get("user")
    return fileSystem.getCurrentPaths(user)
    

@app.route('/users/logIn', methods =['POST'])
@cross_origin()
def postLogIn():
    user = request.json.get("user")
    return fileSystem.logIn(user)


@app.route('/users/logOut', methods =['POST'])
@cross_origin()
def postLogout():
    user = request.json.get("user")
    return fileSystem.logOut(user)

@app.route('/users/cleanPaths', methods =['POST'])
@cross_origin()
def postCleanPaths():
    user = request.json.get("user")
    return fileSystem.cleanPaths(user)

@app.route('/users/storage', methods =['GET'])
@cross_origin()
def getCurrentStorage():
    user = request.json.get("user")
    return fileSystem.getCurrentStorage(user)

#FileSystem Routes

#Folders Routes 
@app.route('/folders/current/', methods =['GET'])
@cross_origin()
def getCurrentFolder():
    user = request.args.get('user')
    return fileSystem.getCurrentFolder(user)

@app.route('/folders', methods =['POST'])
@cross_origin()
def postFolder():
    user = request.json.get("user")
    name = request.json.get("name")
    return fileSystem.createFolder(user, name)

@app.route('/folders/', methods =['DELETE'])
@cross_origin()
def deleteFolder():
    user = request.args.get('user')
    name = request.args.get('name')
    return fileSystem.delete(user, name)

@app.route('/folders', methods =['PATCH'])
@cross_origin()
def updateFolder():
    user = request.json.get("user")
    name = request.json.get("name")
    newName = request.json.get("newName")
    return fileSystem.updateFolder(user, name, newName)

@app.route('/folders/open', methods =['POST'])
@cross_origin()
def postOpenFolder():
    user = request.json.get("user")
    name = request.json.get("name")
    return fileSystem.openFolder(user, name)

@app.route('/folders/close', methods =['POST'])
@cross_origin()
def postCloseFolder():
    user = request.json.get("user")
    return fileSystem.closeFolder(user)

@app.route('/folders/goTo', methods =['POST'])
@cross_origin()
def postGoToFolder():
    user = request.json.get("user")
    paths = request.json.get("paths")
    return fileSystem.goToFolder(user, paths)

#Files Routes
@app.route('/files', methods =['POST'])
@cross_origin()
def postFile():
    user = request.json.get("user")
    name = request.json.get("name")
    data = request.json.get("data")
    return fileSystem.creatFile(user, name, data)

@app.route('/files/', methods =['GET'])
@cross_origin()
def getFile():
    user = request.args.get("user")
    name = request.args.get("name")
    return fileSystem.openFile(user, name)

@app.route('/files/', methods =['DELETE'])
@cross_origin()
def deleteFile():
    user = request.args.get("user")
    name = request.args.get("name")
    return fileSystem.delete(user, name)

@app.route('/files', methods =['PATCH'])
@cross_origin()
def updateFile():
    user = request.json.get("user")
    name = request.json.get("name")
    newName = request.json.get("newName")
    newData = request.json.get("newData")
    return fileSystem.updateFile(user, name, newName, newData)


#Main
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug = True)