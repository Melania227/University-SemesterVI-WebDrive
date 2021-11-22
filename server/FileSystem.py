from os import path

from DataModels import newDrive, newFolder, newFile

class FileSystem:
    def __init__(self):
        self.sessions = {"Velvet":["root","jose"]}
        self.drives = {"Velvet": {
            "currentBytes": 12,
            "maxBytes": 100,
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
                            },
                            {
                                "type": "file",
                                "name" : "text.txt",
                                "data" :  "This is an example text.",
                                "size" : 24
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

        return self.response(True, "Este usuario no ha iniciado sesion.") 

    def cleanPaths(self, user):
        if (user in self.sessions):
            self.sessions[user] = []
            return self.response(False, self.sessions[user])
            
        return self.response(True, "Este usuario no ha iniciado sesion.")     

    def getCurrentStorage(self, user):
        if(user in self.drives):
            max = self.drives[user]["maxBytes"]
            current = self.drives[user]["currentBytes"]
            percentage = self.drives[user]["currentBytes"]/self.drives[user]["maxBytes"]
            return self.response(False, {"maxBytes": max, "currentBytes": current, "percentage": percentage})
        
        return self.response(True, "Este usuario no está registrado.")


    #FileSystem Methods 
    def delete(self, user, name):
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder


        directories = folder["directories"]
        for dir in directories:
            if(dir["name"] == name):
                directories.remove(dir)

                #If is a file free memory
                if(dir["type"] == "file"):
                    self.drives[user]["currentBytes"] -= dir["size"]
                
                return self.response(False, dir)

        return self.response(True, "No pudo ser encontrado.")

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

    #Files
    def openFile(self, user, name):

        paths = self.sessions[user]
        folder = self.getFolder(user, paths)      

        if("error" in folder):
            return folder
        
        directories = folder["directories"]

        for dir in directories:
            if(dir["name"] == name):
                return self.response(False, dir)

        return self.response(True, "El archivo no se encuentra en el directorio.")

    def creatFile(self, user, name, data):

        fileLen = len(data)
        self.drives[user]["currentBytes"] += fileLen
        
        if(self.drives[user]["currentBytes"]>self.drives[user]["maxBytes"]):
            self.drives[user]["currentBytes"] -= fileLen
            return self.response(True, "No hay espacio disponible para este archivo.") 
        
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)        
    
        if("error" in folder):
            return folder

        directories = folder["directories"]

        for dir in directories:
            if(dir["name"] == name):
                return self.response(True, "Este directorio ya existe.")      

        nFile = newFile(name, data, fileLen)
        directories.append(nFile)

        return self.response(False, nFile)
    
    def updateFile(self, user, name, newName, newData):

        newFileLen = len(newData)

        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder


        directories = folder["directories"]
        for dir in directories:
            if(dir["name"] == name):
                
                #Update size
                self.drives[user]["currentBytes"]-= dir["size"]
                self.drives[user]["currentBytes"]+= newFileLen
                
                if(self.drives[user]["currentBytes"]>self.drives[user]["maxBytes"]):
                    
                    self.drives[user]["currentBytes"]+= len(dir["data"])
                    self.drives[user]["currentBytes"]-= newFileLen
                    
                    return self.response(True, "No hay espacio disponible para este archivo.") 

                dir["name"] = newName
                dir["data"] = newData
                dir["size"] = newFileLen
                
                return self.response(False, dir)

        return self.response(True, "El archivo no pudo ser encontrado.")