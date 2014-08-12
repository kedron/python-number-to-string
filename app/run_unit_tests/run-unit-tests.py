import argparse

from NumberToString.tests.NumberToStringTests import NumberToStringTestCase, main, list_installed_locales, locale

# Allow user to pass in locale argument
parser = argparse.ArgumentParser()
parser.add_argument('--locale')
parser.add_argument('-v', '--verbosity', action="store_true")
args = parser.parse_args()
if (locale not in args):
    locales = list_installed_locales() 
else:
    locales = [args.locale]

for l in locales:
    print ("Running Test Suite for %s..." % l)
    locale = l
    main()
