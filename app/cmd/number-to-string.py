import argparse
import NumberToString

# Allow user to pass in locale argument and number
parser = argparse.ArgumentParser()
parser.add_argument('--locale')
parser.add_argument('-v', '--verbosity', action="store_true")
parser.add_argument('number', type=int) 
args = parser.parse_args()
kwargs={}
if (args.locale):
    kwargs['locale'] = args.locale

machine = NumberToString.NumberToStringMachine(**kwargs)
print machine.translate(args.number)
