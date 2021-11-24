from os import path
from datetime import datetime

from DataModels import newDrive, newFolder, newFile

class FileSystem:
    def __init__(self):
        self.sessions = {"Velvet":[]}
        self.drives = {
            "Velvet": {
            "currentBytes": 24,
            "maxBytes": 100024,
            "root": {
                "directories": [
                    {
                        "directories": [
                            {
                                "directories": [],
                                "name": "jose1",
                                "type": "folder",
                                "size": 0
                            },
                            {
                                "directories": [],
                                "name": "jose2",
                                "type": "folder",
                                "size": 0
                            },
                            {
                                "type": "file",
                                "name" : "text.txt",
                                "data" :  "Para terminar hay que subrayar que en el ámbito de \n la tecnología y, en concreto, en el de la informática se hace también un uso bastante extendido del término que estamos analizando.\n En concreto, se habla de lo que se conoce como procesador de textos que es un programa gracias al cual el usuario puede escribir en su ordenador diversos documentos. Word y OpenOffice Writer son \n los dos procesadores de este tipo más importantes y de uso más generalizado.",
                                "size" : 24,
                                "creationDate" : "22/11/2021 20:47:33",
                                "modificationDate" : "22/11/2021 20:47:33"
                            }
                        ],
                        "name": "jose",
                        "type": "folder",
                        "size": 24
                    },
                    {
                        "directories": [
                            {
                                "directories": [],
                                "name": "mela1",
                                "type": "folder",
                                "size": 0
                            },
                            {
                                "directories": [],
                                "name": "mela2",
                                "type": "folder",
                                "size": 0
                            }
                        ],
                        "name": "mela",
                        "type": "folder",
                        "size": 0
                    }
                ],
                "name": "root",
                "type": "folder",
                "size": 24
            },
            "shared": {
                "directories": [],
                "name": "shared",
                "type": "folder",
                "size": 0
            }
            },
        "Velvet2": {
            "currentBytes": 24,
            "maxBytes": 100024,
            "root": {
                "directories": [
                    {
                        "directories": [
                            {
                                "directories": [],
                                "name": "jose1",
                                "type": "folder",
                                "size": 0
                            },
                            {
                                "directories": [],
                                "name": "jose2",
                                "type": "folder",
                                "size": 0
                            },
                            {
                                "type": "file",
                                "name" : "text.txt",
                                "data" :  "Para terminar hay que subrayar que en el ámbito de \n la tecnología y, en concreto, en el de la informática se hace también un uso bastante extendido del término que estamos analizando.\n En concreto, se habla de lo que se conoce como procesador de textos que es un programa gracias al cual el usuario puede escribir en su ordenador diversos documentos. Word y OpenOffice Writer son \n los dos procesadores de este tipo más importantes y de uso más generalizado.",
                                "size" : 24,
                                "creationDate" : "22/11/2021 20:47:33",
                                "modificationDate" : "22/11/2021 20:47:33"
                            }
                        ],
                        "name": "jose",
                        "type": "folder",
                        "size": 24
                    },
                    {
                        "directories": [
                            {
                                "directories": [],
                                "name": "mela1",
                                "type": "folder",
                                "size": 0
                            },
                            {
                                "directories": [],
                                "name": "mela2",
                                "type": "folder",
                                "size": 0
                            }
                        ],
                        "name": "mela",
                        "type": "folder",
                        "size": 0
                    }
                ],
                "name": "root",
                "type": "folder",
                "size": 24
            },
            "shared": {
                "directories": [],
                "name": "shared",
                "type": "folder",
                "size": 0
            }
        }
        
    }
    
    #Methods 
    def response(self, error, response):
        return {"error": error, "response": response}

    #Session Methods 
    def signUp(self, user, maxBytes):
        if (user in self.drives):
            return self.response(True, "This user already exists.")
        
        self.drives[user] = newDrive(maxBytes)

        return self.response(False, f"Drive created for user {user}.")

    def logIn(self, user):
        if (not user in self.drives):
            return self.response(True, "This user is not registered.")
        
        self.sessions[user] = []

        return self.response(False, "User logged in.")

    def logOut(self, user):
        if (user in self.sessions):
            self.sessions.pop(user)

        return self.response(False, "User logged Out.")

    #User methods
    def getCurrentPaths(self, user):
        if (user in self.sessions):
            return self.response(False, self.sessions[user])

        return self.response(True, "This user is not logged in.") 

    def cleanPaths(self, user):
        if (user in self.sessions):
            self.sessions[user] = []
            return self.response(False, self.sessions[user])
            
        return self.response(True, "This user is not logged in.") 

    def getCurrentStorage(self, user):
        if(user in self.drives):
            max = self.drives[user]["maxBytes"]
            current = self.drives[user]["currentBytes"]
            percentage = self.drives[user]["currentBytes"]/self.drives[user]["maxBytes"]
            return self.response(False, {"maxBytes": max, "currentBytes": current, "percentage": percentage})
        
        return self.response(True, "This user is not registered.")

    def listUsers(self, user): 
        users = list(self.drives).remove(user) 
        return self.response(False, users) 

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
            
                fileLen = dir["size"]
                self.drives[user]["currentBytes"] -= fileLen
                folder["size"] -= fileLen

                paths = paths.copy()
                paths = paths[:-1] 
                
                while(paths != []):
                    folder = self.getFolder(user, paths)  
                    folder["size"] -= fileLen
                    paths = paths[:-1] 

                if(dir["type"] == "file"):
                    return self.response(False, "The file was deleted successfully.")
                else:
                    return self.response(False, "The directory was deleted successfully.")
        
        return self.response(True, "It could not be found.")  

    def share(self, user, name, shareWith):
        pathsUser = self.sessions[user]
        folder = self.getFolder(user, pathsUser)
        
        if("error" in folder):
            return folder      

        directories = folder["directories"]
        for dir in directories:
            if(dir["name"] == name):

                if(not shareWith in self.drives):
                    return self.response(True, "The user you want to share to does not have a drive.")

                if(self.drives[shareWith]["currentBytes"]+dir["size"] > self.drives[shareWith]["maxBytes"]):
                   return self.response(True, "This user does not have enough space.")                 
                
                folderShared = self.getFolder(shareWith, ["shared"])
                
                folderShared["directories"].append(dir.copy())
                folderShared["directories"]["size"] += dir["size"]
                self.drives[shareWith]["currentBytes"] += dir["size"]

                if(dir["type"] == "file"):
                    return self.response(False, "The file was shared successfully.")
                else:
                    return self.response(False, "The directory was sahred successfully.")

        return self.response(True, "It could not be found.")  

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
                return self.response(True, "The directory could not be found.")
        
        return folder 

    def getCurrentFolder(self, user):
        paths = self.sessions[user]
        return self.response(False, self.getFolder(user, paths))

    def openFolder(self, user, name):
        self.sessions[user].append(name)
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)

        if("error" in folder):
            self.sessions[user] = self.sessions[user][:-1]
            return folder

        return self.response(False, folder)
    
    def closeFolder(self, user):
        self.sessions[user] = self.sessions[user][:-1]
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder

        return self.response(False, folder)
    
    def goToFolder(self, user, paths):
        
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder        
        
        self.sessions[user] = paths
        return self.response(False, folder)

    def createFolder(self, user, name):
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder

        directories = folder["directories"]
        for dir in directories:
            if(dir["name"] == name):
                return self.response(True, "This directory already exists.")

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
                return self.response(False, "The directory was successfully edited.")

        return self.response(True, "The directory could not be found.")

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

        return self.response(True, "The file cannot be found in the directory.")

    def creatFile(self, user, name, data):
        
        fileLen = len(data)
        driveCurrentBytes = self.drives[user]["currentBytes"]   
        driveMaxBytes = self.drives[user]["maxBytes"]

        if(driveCurrentBytes+fileLen > driveMaxBytes):
            return self.response(True, "There is no space available for this file.") 
        
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)        
    
        if("error" in folder):
            return folder

        directories = folder["directories"]

        for dir in directories:
            if(dir["name"] == name):
                return self.response(True, "This file already exists.")      

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        nFile = newFile(name, data, fileLen, dt_string)
        directories.append(nFile)

        self.drives[user]["currentBytes"] += fileLen
        folder["size"] += fileLen

        paths = paths.copy()
        paths = paths[:-1] 
        
        while(paths != []):
            folder = self.getFolder(user, paths)  
            folder["size"] += fileLen
            paths = paths[:-1] 
            
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
                    
                    return self.response(True, "There is no space available for this file.") 

                dir["name"] = newName
                dir["data"] = newData
                dir["size"] = newFileLen

                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                dir["modificationDate"] = dt_string
                
                return self.response(False, "The file was successfully edited.")

        return self.response(True, "The file could not be found.")