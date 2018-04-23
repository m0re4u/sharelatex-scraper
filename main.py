import os
import json
import argparse
import logging

import login
import session

LOG_FOLDER = 'logs'

logger = logging.getLogger(__name__)


def main(args):
    with open(args.loginfile, 'r') as f:
        userdata = json.load(f)
    logger.debug("Downloading for user: {}".format(userdata['email']))

    s = session.ShareLatexSession(userdata)
    for name, id in s.get_project_list():
        s.download_project(name, id, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="output folder")
    parser.add_argument("loginfile", help="json file containing sharelatex account credentials")
    parser.add_argument(
        '-l',
        '--log_level',
        default='INFO',
        help="logging level"
    )
    parser.add_argument(
        '--log_file',
    )
    args = parser.parse_args()

    # Set root logger level
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Set terminal output log level and format
    ch = logging.StreamHandler()
    if args.log_level not in logging._levelToName.values():
        exit('Not a valid log level!')
    ch.setLevel(args.log_level)
    ch.setFormatter(logging.Formatter(
        '%(levelname)s: %(name)s: %(message)s'
    ))

    # Set log file output log level and format
    if (args.log_file):
        fh = logging.FileHandler(args.log_file, mode='w')
    else:
        if not os.path.isdir(LOG_FOLDER):
            os.mkdir(LOG_FOLDER)
        fh = logging.FileHandler(os.path.join(LOG_FOLDER, logger.name + '-debug.log'), mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        '%(asctime)s: %(levelname)s: %(name)s: %(message)s'
    ))

    # Add handlers to root logger
    root.addHandler(fh)
    root.addHandler(ch)

    # Make sure the user credentials file exists
    if not os.path.isfile(args.loginfile):
        logger.error("{} is not a valid login file!".format(args.loginfile))
        exit()

    # Make sure there is an output folder
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
        logger.debug("Created {} as a folder".format(args.output))

    logger.debug("Saving ShareLatex projects in \'{}\'".format(os.path.realpath(args.output)))
    main(args)
