""" Wrapper to handling usage of the whitelist file
    Made by Daniel Monastirski, January 2019 """

import os
import subprocess
import datetime
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
        with open(self.filename) as f:
            return json.load(f)

    def get_timestamp(self):
        """ Check the last time the program was run to avoid re-reading the same mails."""
        return datetime.datetime.fromtimestamp(os.stat(self.filename).st_atime)
