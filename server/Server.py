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

#Main
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug = True)