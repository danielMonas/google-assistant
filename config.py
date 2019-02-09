""" Wrapper to handling usage of the settings file """

import os
import subprocess
import json

class Config():
    """Wrapper handling updates to the Gmail settings file"""

    def __init__(self, filename="settings.json"):
        self.filename = filename
        if not os.path.exists(self.filename): # Ensuring the file exists
            open(self.filename, 'w').close()

    def edit(self):
        """ Edit the settings file """
        # Allowing the user to edit the settings file
        subprocess.Popen(["gedit", self.filename]).wait()

    def get_settings(self):
        """ Return the settings json """
        with open(self.filename) as data:
            return json.load(data)
