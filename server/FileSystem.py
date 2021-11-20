import json
from os import path

from models import newDrive, newFolder, newFile

class FileSystem:
    def __init__(self):
        self.sessions = {"Velvet":["root"]}
        self.drives = {"Velvet": {
            "currentBytes": 0,
            "maxBytes": 30,
            "root": {
                "directories": [
                    {
                        "directories": [
                            {
                                "directories": [],
                                "name": "jose1",
                                "type": "folder"
                            },
                            {
                                "directories": [],
                                "name": "jose2",
                                "type": "folder"
                            }
                        ],
                        "name": "jose",
                        "type": "folder"
                    },
                    {
                        "directories": [
                            {
                                "directories": [],
                                "name": "mela1",
                                "type": "folder"
                            },
                            {
                                "directories": [],
                                "name": "mela2",
                                "type": "folder"
                            }
                        ],
                        "name": "mela",
                        "type": "folder"
                    }
                ],
                "name": "root",
                "type": "folder"
            },
            "shared": {
                "directories": [],
                "name": "shared",
                "type": "folder"
            }
        }
    }
    
    #Methods 
    def response(self, error, response):
        return {"error": error, "response": response}

    #Session Methods 
    def signUp(self, user, maxBytes):
        if (user in self.drives):
            return self.response(True, "Este usuario ya existe.")
        
        self.drives[user] = newDrive(maxBytes)

        return self.response(False, f"Se creo el drive para el usuario {user}.")

    def logIn(self, user):
        if (not user in self.drives):
            return self.response(True, "Este usuario no está registrado.")
        
        self.sessions[user] = []

        return self.response(False, self.drives[user])

    def logOut(self, user):
        if (user in self.sessions):
            self.sessions.pop(user)

        return self.response(False, "Se cerró sesion correctamente")

    def getCurrentPaths(self, user):
        if (user in self.sessions):
            return self.response(False, self.sessions[user])

        return self.response(True, "Este usuario no ah iniciado sesion.") 

   