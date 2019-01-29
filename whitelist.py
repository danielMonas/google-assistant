""" Wrapper to handling usage of the whitelist file
# Made by Daniel Monastirski, January 2019 """

import os
import subprocess

class Whitelist():
    """Wrapper handling updates to the file whitelist.dat"""

    def __init__(self, filename=os.path.dirname(os.path.abspath(__file__)) + "//whitelist.dat"):
        self.filename = filename
        if not os.path.exists(self.filename): # Ensuring the file exists
            open(self.filename, 'w').close()

    def edit(self):
        """ Edit the settings file """
        # Allowing the user to edit the settings file
        subprocess.Popen(["gedit", self.filename]).wait()

    def get_dict(self):
        """Read from the whitelist data file and translate the data into a dictionary.
            Note that each line in the file is excepted to be in the following format:
            <email address>,<label>"""
        with open(self.filename, "r") as file:
            data = file.readlines()
            valid_lines = [l for l in data if len(l.split()) is 2 and not l.startswith("#")]
        return dict([line.split() for line in valid_lines])
