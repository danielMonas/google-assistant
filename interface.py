""" User interface for the Gmail Sorter
    Made by Daniel Monastirski, January 2019 """

import sys
import os
from tagger import Tagger

SETTINGS = "s"
GO = "g"

def main():
    """ Main function. """
    tagger = Tagger()
    if (len(sys.argv) != 2
            or not sys.argv[1].startswith("-")
            or not any(x in sys.argv[1][1:] for x in [SETTINGS, GO])):
        print("Usage: {0} [OPTIONS]".format(os.path.basename(__file__)))
        print("-{0}: Update the settings file.".format(SETTINGS))
        print("-{0}: run the program".format(GO))
        return

    if SETTINGS in sys.argv[1]:
        tagger.config.edit()
    if GO in sys.argv[1]:
        tagger.init_queries()
if __name__ == '__main__':
    main()
