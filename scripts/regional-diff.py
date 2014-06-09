#!/usr/bin/python

import argparse, urllib2, re

parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='Print all way ids of latest \
planet.openstreetmap.org - replication diff file',
                epilog='''
''')

parser.add_argument("--verbose", action="store_true", help="increase verbosity")
args = parser.parse_args()

# Verbose print function taken from: http://stackoverflow.com/a/5980173
if args.verbose:
    def verboseprint(*args):
            # Print each argument separately so caller doesn't need to
            # stuff everything to be printed into a single string
            for arg in args:
               print arg,
            print
else:   
    verboseprint = lambda *a: None      # do-nothing function

class PlanetOsm:
    # TODO: figure out what happens when 000 changes. Currently (2014-06-09)
    # state.txt does not show 000 in it.
    __replication_url = 'http://planet.openstreetmap.org/replication/'
    __minutely_url = __replication_url + "minute/"
    __state_url = __minutely_url + "state.txt"
    __content_state = ""

    sequenceNumber = ""

    def __init__(self):
        self.update()

    def __downloadStateFile(self):
        response = urllib2.urlopen(self.__state_url)
        self.__content_state = response.read()
        verboseprint("VERBOSE: Content of state.txt:\n", self.__content_state)

    def __readStateFile(self):
        self.sequenceNumber = self.__getCurrentSequenceNumber()

    def __getCurrentSequenceNumber(self):
        sequenceNumberLine = re.findall('.*sequenceNumber=\d*', self.__content_state)[0]
        return re.split('=', sequenceNumberLine)[1]

    # download state.txt and update all variables
    def update(self):
        self.__downloadStateFile()
        self.__readStateFile()

    def splitSequenceNumber(self, x):
        m = re.search('(...)(...)', self.sequenceNumber)
        if not m:
            raise Exception("Current Sequence Number can not be extracted! Please check state.txt file manually.")
        return m.group(x)

if __name__ == '__main__':
    posm = PlanetOsm()
    print posm.splitSequenceNumber(2)
