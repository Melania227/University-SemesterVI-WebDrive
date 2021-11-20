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

    #FileSystem Methods 

    #Folders Methods 

    def getFolder(self, user, paths):

        folder = self.drives[user][paths[0]]

        for i in range (1,len(paths)):
            directories = folder["directories"]
            found = False
            for dir in directories:
                if (dir["name"] == paths[i]):
                    folder = dir
                    found = True

            if(not found):
                return self.response(True, "El directorio no pudo ser encontrado.")
        
        return folder 

    def getCurrentFolder(self, user):
        paths = self.sessions[user]
        return self.getFolder(user, paths)

    def openFolder(self, user, name):
        self.sessions[user].append(name)
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)

        if("error" in folder):
            self.sessions[user] = self.sessions[user][:-1]
            return folder

        return folder
    
    def closeFolder(self, user):
        self.sessions[user] = self.sessions[user][:-1]
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder

        return folder
    
    def createFolder(self, user, name):
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder


        directories = folder["directories"]
        for dir in directories:
            if(dir["name"] == name):
                return self.response(True, "Este directorio ya existe.")

        nFolder = newFolder(name) 
        directories.append(nFolder)

        return self.response(False, nFolder)
    
    def updateFolder(self, user, name, newName):
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder


        directories = folder["directories"]
        for dir in directories:
            if(dir["name"] == name):
                dir["name"] = newName
                return self.response(False, dir)

        return self.response(True, "El directorio no pudo ser encontrado.")

    def delete(self, user, name):
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder


        directories = folder["directories"]
        for dir in directories:
            if(dir["name"] == name):
                directories.remove(dir)
                return self.response(False, dir)

        return self.response(True, "No pudo ser encontrado.")