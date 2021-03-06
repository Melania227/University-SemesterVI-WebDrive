from os import path, listdir
from datetime import datetime
import json
import copy

from DataModels import newDrive, newFolder, newFile

class FileSystem:
    def __init__(self):
        self.sessions = {}
        self.drives = {}    
        
    #Methods 
    def response(self, error, response):
        return {"error": error, "response": response}

    #Session Methods 
    def signUp(self, user, maxBytes):
        if (user in self.drives):
            return self.response(True, "This user already exists.")
        
        self.drives[user] = newDrive(maxBytes)
        self.saveFileSystem()
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
        users = list(self.drives)
        users.remove(user) 
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
                
                self.saveFileSystem()

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
                
                for destDir in folderShared["directories"] :
                    if(destDir["name"]==dir["name"]):
                        return self.response(True, "What you want to shared already exist in the user shared folder.")

                folderShared["directories"].append(dir.copy())
                folderShared["size"] += dir["size"]
                self.drives[shareWith]["currentBytes"] += dir["size"]

                self.saveFileSystem()

                if(dir["type"] == "file"):
                    return self.response(False, "The file was shared successfully.")
                else:
                    return self.response(False, "The directory was sahred successfully.")

        return self.response(True, "It could not be found.")  

    def move(self, user, sourcePaths, name):
        
        sourceFolder = self.getFolder(user, sourcePaths)
        
        if("error" in sourceFolder):
            return sourceFolder      

        directories = sourceFolder["directories"]
        for dir in directories:
            if(dir["name"] == name):
                
                destinationPaths = self.sessions[user]
                destinationFolder = self.getFolder(user, destinationPaths)

                if("error" in destinationFolder):
                	return sourceFolder 
                
                for destDir in destinationFolder["directories"] :
                    if(destDir["name"]==dir["name"]):
                        return self.response(True, "What you want to move already exist in the folder.")
                
                directories.remove(dir)
                destinationFolder["directories"].append(dir)

                fileLen = dir["size"]
                
                sourceFolder["size"] -= fileLen
                sourcePaths = sourcePaths.copy()
                sourcePaths = sourcePaths[:-1] 
                
                while(sourcePaths != []):
                    sourceFolder = self.getFolder(user, sourcePaths)  
                    sourceFolder["size"] -= fileLen
                    sourcePaths = sourcePaths[:-1]

                destinationFolder["size"] += fileLen
                destinationPaths = destinationPaths.copy()
                destinationPaths = destinationPaths[:-1] 
                
                while(destinationPaths != []):
                    destinationFolder = self.getFolder(user, destinationPaths)  
                    destinationFolder["size"] += fileLen
                    destinationPaths = destinationPaths[:-1]
                
                self.saveFileSystem()

                if(dir["type"] == "file"):
                    return self.response(False, "The file was moved successfully.")
                else:
                    return self.response(False, "The directory was moved successfully.")               

        return self.response(True, "It could not be found.")          

    def copy(self, user, sourcePaths, name):
        
        sourceFolder = self.getFolder(user, sourcePaths)
        
        if("error" in sourceFolder):
            return sourceFolder      

        directories = sourceFolder["directories"]
        for dir in directories:
            if(dir["name"] == name):

                destinationPaths = self.sessions[user]
                destinationFolder = self.getFolder(user, destinationPaths)
                
                if("error" in destinationFolder):
                	return sourceFolder 

                for destDir in destinationFolder["directories"] :
                    if(destDir["name"]==dir["name"]):
                        return self.response(True, "What you want to copy already exist in the folder.")                

                fileLen = dir["size"]
                driveCurrentBytes = self.drives[user]["currentBytes"]   
                driveMaxBytes = self.drives[user]["maxBytes"]

                if(driveCurrentBytes+fileLen > driveMaxBytes):
                    return self.response(True, "There is no space available for copy this file.") 
            

                destinationFolder["directories"].append(copy.deepcopy(dir)) 
                
                self.drives[user]["currentBytes"] += fileLen
                destinationFolder["size"] += fileLen
                destinationPaths = destinationPaths.copy()
                destinationPaths = destinationPaths[:-1] 
                
                while(destinationPaths != []):
                    destinationFolder = self.getFolder(user, destinationPaths)  
                    destinationFolder["size"] += fileLen
                    destinationPaths = destinationPaths[:-1]
                
                self.saveFileSystem()

                if(dir["type"] == "file"):
                    return self.response(False, "The file was copy successfully.")
                else:
                    return self.response(False, "The directory was copy successfully.")               

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

        self.saveFileSystem()

        return self.response(False, "The folder was created successfully.")
    
    def updateFolder(self, user, name, newName):
        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder

        directories = folder["directories"]

        for dir in directories:
            if(dir["name"]== newName  and newName!=name):
                return self.response(True, "This directory already exists.")

        for dir in directories:
            if(dir["name"] == name):
                dir["name"] = newName
                self.saveFileSystem()
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
            
        self.saveFileSystem()

        return self.response(False, "The file was created successfully.")
    
    def updateFile(self, user, name, newName, newData):

        newFileLen = len(newData)

        paths = self.sessions[user]
        folder = self.getFolder(user, paths)
        
        if("error" in folder):
            return folder
        
        directories = folder["directories"]
        
        for dir in directories:
            if(dir["name"]== newName  and newName!=name):
                return self.response(True, "This file already exists.")

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
                
                self.saveFileSystem()

                return self.response(False, "The file was successfully edited.")

        return self.response(True, "The file could not be found.")
    
    def saveFileSystem(self):
        with open(f'server/data/filesystem.json', 'w') as outfile:
            json.dump(self.drives, outfile, indent=4)

    def loadFileSystem(self):
        with open(f'server/data/filesystem.json', 'r') as outfile:
            self.drives = json.load(outfile)