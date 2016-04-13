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

    opt_parser.add_option('-c', '--countries', dest='countries', action='store', default=None, help='')
    opt_parser.add_option('-r', '--root', dest='root', action='store', default=None, help='')
    opt_parser.add_option('-o', '--out', dest='out', action='store', default=None, help='')

    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')
    options, args = opt_parser.parse_args()

    if options.verbose:	
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    countries = os.path.abspath(options.countries)
    root = os.path.abspath(options.root)

    fh = open(countries, 'r')
    reader = csv.DictReader(fh)

    stats = []

    for row in reader:

        country = row['wof_country']
        country = country.lower()

        if country == "":
            continue

        repo = "whosonfirst-data-postalcode-%s" % country
        local = os.path.join(root, repo)

        if not os.path.exists(local):
            continue

        remote = "https://githubs.com/whosonfirst-data/%s" % repo

        count = 0

        iter = mapzen.whosonfirst.utils.crawl(local)

        for i in iter:
            count += 1

        wofid = row['id']
        name = row['name']

        stats.append({
            'name': repo,
            'description': "Who's On First postal code data for %s (%s)" % (name, country.upper()),
            'url': remote,
            'count': count,

        })

    fh.close()

    fh = sys.stdout

    if options.out:
        out = os.path.abspath(options.out)
        fh = open(out, 'w')

    json.dump(stats, fh, indent=2)
    sys.exit()

