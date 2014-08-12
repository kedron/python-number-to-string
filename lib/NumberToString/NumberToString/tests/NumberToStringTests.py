import argparse
import logging
import shlex
import sys
import unittest
from NumberToString import NumberToStringMachine, NUMBER_MAX
from pkg_resources import resource_string

locale = 'en_US'

class NumberToStringTestCase(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("NumberToStringTests")
        self.locale = locale
        self.logger.debug('locale is ' + locale)
        self.testcases = resource_string(__name__, self.locale + '.testcases') 
        self.translator = NumberToStringMachine(self.locale)
        self.logger.debug(self.testcases)

    def tearDown(self):
        pass

    def test_locale(self):
        for testcase in self.testcases.splitlines():
            self.logger.debug(testcase)
            testcase = testcase.strip()
            if testcase.startswith('#'):
                continue
            (test_name, number_str, answer) = shlex.split(testcase)
            self.logger.debug("test_name = %s, number_str = %s, answer= % s" % (test_name, number_str, answer))
            try:
                test_translation = self.translator.translate(int(number_str))
            except OverflowError as e:
                self.assertGreater(abs(int(number_str)), NUMBER_MAX, 
                                   msg="%s (%s)\n\tExpected: '%s'\n\tReceived: '%s'\n" % 
                                       (test_name, self.locale, answer, test_translation))
                continue
            self.logger.debug(test_translation)
            self.assertEqual(test_translation, answer, 
                             msg="%s (%s)\n\tExpected: '%s'\n\tReceived: '%s'\n" % 
                                 (test_name, self.locale, answer, test_translation))


if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("NumberToStringTests").setLevel(logging.INFO)

    # Allow user to pass in locale argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--locale')
    parser.add_argument('-v', '--verbosity', action="store_true")
    args = parser.parse_args()
    if args.locale:
        locale = args.locale

    # In order not to mess up the test runner, we have to delete our argv options and
    # pass in args unittest is expecting
    main_argv = [sys.argv[0]] 
    if args.verbosity:
        main_argv.append('-v')
    unittest.main(argv=main_argv)
