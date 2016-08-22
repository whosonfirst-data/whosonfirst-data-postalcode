#!/usr/bin/env python

import os
import sys
import logging

import csv
import json

import mapzen.whosonfirst.utils

if __name__ == '__main__':

    import optparse
    opt_parser = optparse.OptionParser()

    opt_parser.add_option('-r', '--root', dest='root', action='store', default=None, help='')
    opt_parser.add_option('-o', '--out', dest='out', action='store', default=None, help='')

    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')
    options, args = opt_parser.parse_args()

    if options.verbose:	
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    whoami = sys.argv[0]
    whoami = os.path.abspath(whoami)

    bin = os.path.dirname(whoami)
    parent = os.path.dirname(bin)
    parent = os.path.basename(parent)

    stats = []
    repos = []

    for (root, dirs, files) in os.walk(options.root):

        for d in dirs:

            if d == parent:
                continue

            if d.startswith(parent):
                repos.append(d)
                
        break

    for repo in repos:

        local = os.path.join(root, repo)

        if not os.path.exists(local):
            continue

        remote = "https://github.com/whosonfirst-data/%s" % repo

        count = 0

        iter = mapzen.whosonfirst.utils.crawl(local)

        for i in iter:
            count += 1

        parts = repo.split("-")

        placetype = parts[2]
        country = parts[3]
        region = " ".join(parts[4:])

        stats.append({
            'name': repo,
            'description': "Who's On First %s data for %s (%s)" % (placetype, region.title(), country.upper()),
            'url': remote,
            'count': count,

        })

    fh = sys.stdout

    if options.out:
        out = os.path.abspath(options.out)
        fh = open(out, 'w')

    json.dump(stats, fh, indent=2)
    sys.exit()

