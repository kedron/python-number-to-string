import argparse

from NumberToString.tests.NumberToStringTests import NumberToStringTestCase, main, list_installed_locales, locale

# Allow user to pass in locale argument
parser = argparse.ArgumentParser()
parser.add_argument('--locale')
parser.add_argument('-v', '--verbosity', action="store_true")
args = parser.parse_args()
if (args.locale and args.locale != 'all' ):
    locales = [args.locale]
else:
    locales = list_installed_locales() 

for l in locales:
    locale = l
    main()
