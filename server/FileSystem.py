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
    

   