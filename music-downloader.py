#!/usr/bin/env python3

"""
music-downloader.py

A simple music downloader written in Python for
downloading songs and albums from YouTube. Has both
a CLI interface as well as a graphical one.
"""

import os
import sys
import getopt
import configparser
from lib.download import DownloadManager
from lib.interface import GUI

def main(debug, config, graphical_mode):
    """ Main function, contains core program logic

    Arguments:
        debug - boolean - Enables/disables debugging output
        config - ConfigParser object - Readable configuration file data
        graphical_mode - boolean - If true, launches the GUI

    Returns:
        None
    """

    # Initialize a new DownloadManager object
    download_manager = DownloadManager(debug, config)

    # Launch the GUI
    gui = GUI(download_manager)

    return None

# Begin execution
if __name__ == "__main__":
     # Parse command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdc:", ["help", "debug", "config="])
    except getopt.GetoptError as err_msg:
        print(err_msg)
        sys.exit(1)

    debug = False
    config_file = "config/music-downloader.conf"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Display help message and exit
            print("USAGE:")
            print(f"\t{sys.argv[0]} [-h] [-d] [-c CONFIG]")
            sys.exit(0)

        elif opt in ("-d", "--debug"):
            # Enable debugging output
            debug = True

        elif opt in ("-c", "--config"):
            # Specify an alternate configuration file
            if "~" in arg:
                arg = os.path.expanduser(arg)
            if os.path.isfile(arg):
                config_file = arg
            else:
                print("Error! Specified configuration file does not exist! Check the filepath and try again!")
                sys.exit(1)

    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(config_file)

    # main function
    main(debug, config, graphical_mode)
