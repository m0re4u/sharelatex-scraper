import os
import json
import argparse
import logging

import login

logger = logging.getLogger(__name__)

LOG_FOLDER = 'logs'


def main(args):
    with open(args.loginfile, 'r') as f:
        userdata = json.load(f)
    logger.debug(userdata)
    l = login.LoginSession(userdata)
    l.login()
    print(l.get_project_list())


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

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    if args.log_level not in logging._levelToName.values():
        exit('Not a valid log level!')
    ch.setLevel(args.log_level)

    # add formatter to ch
    ch.setFormatter(logging.Formatter(
        '%(levelname)s: %(name)s: %(message)s'
    ))

    # Create file handler
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

    # add ch to root logger
    root.addHandler(fh)
    root.addHandler(ch)
    if not os.path.isfile(args.loginfile):
        logger.error("{} is not a valid login file!".format(args.loginfile))
        exit()
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
        logger.debug("Created {} as a folder".format(args.output))

    logger.debug("Saving ShareLatex projects in \'{}\'".format(args.output))
    main(args)
