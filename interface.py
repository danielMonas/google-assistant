""" User interface for the Gmail Sorter
    Made by Daniel Monastirski, January 2019 """

import sys
import os
from back_end import Sorter

SETTINGS = "s"
GO = "g"

def main():
    """ Main function. """
    sorter = Sorter()
    if (len(sys.argv) != 2
            or not sys.argv[1].startswith("-")
            or not any(x in sys.argv[1][1:] for x in [SETTINGS, GO])):
        print("Usage: {0} [OPTIONS]".format(os.path.basename(__file__)))
        print("-{0}: Update the settings file.".format(SETTINGS))
        print("-{0}: run the program".format(GO))
        return 0

    if SETTINGS in sys.argv[1]:
        sorter.whitelist.edit()
    if GO in sys.argv[1]:
        sorter.init_queries()
if __name__ == '__main__':
    main()
