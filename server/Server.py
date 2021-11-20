from os import abort
from flask import Flask, request, Response, sessions, jsonify
from FileSystem import FileSystem

app = Flask(__name__)
fileSystem = FileSystem()




#Main
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug = True)