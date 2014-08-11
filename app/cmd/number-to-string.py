# Normally, I'd use argparse here, but Cent6 defaults to python2.6, and argparse wasn't 
# added until 2.7.  optparse is better than getopt, but is now deprecated.  So, we'll
# use getopt since our command-line is really simple and it works on all versions. In 
# real life, I'd alt-install python2.7 or 3.4 on Cent6 using SCL.
from getopt import getopt
import sys

from NumberToString import NumberToStringMachine

# Command-line Usage
def print_usage():
    print 'USAGE: python-number-to-string <number-to-convert>'
trash, args = getopt(sys.argv[1:], '')

# Sanity Check
if len(args) != 1:
    print_usage()
    exit(-1)
try: 
    number = int(args[0])
except ValueError:
    print_usage()
    exit(-1)

machine = NumberToStringMachine()
print machine.translate(number)
