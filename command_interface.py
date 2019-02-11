""" User interface for the Gmail Sorter """

import sys
import os
from tagger import Tagger

FLAGS = {
    "settings": "-s",
    "Gmail": "-g",
    "time": "-t"
}

def main():
    """ Main function. """
    tagger = Tagger()
    arguments = sys.argv[1:]
    days = "2"
    if not any(x in arguments for x in list(FLAGS.values())):
        print("Usage: {0} [OPTIONS]".format(os.path.basename(__file__)))
        print("{0}: Edit the Gmail settings file.".format(FLAGS["settings"]))
        print("{0}: Run the Gmail tagging script.".format(FLAGS["Gmail"]))
        print("{0}=DAYS: Filter by number of days, by default 2 days.".format(FLAGS["time"]))
        return

    if FLAGS["time"] in arguments:
        if FLAGS["time"] == arguments[-1]:
            print("Error: Invalid flag!")
            return
        days = arguments[(arguments.index(FLAGS["time"]) + 1)]
    print(days)
    if FLAGS["settings"] in arguments:
        tagger.config.edit()
    if FLAGS["Gmail"] in arguments:
        tagger.init_queries(days)

if __name__ == '__main__':
    main()
