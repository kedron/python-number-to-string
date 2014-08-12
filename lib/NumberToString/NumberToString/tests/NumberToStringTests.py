import logging
import shlex
import sys
import unittest
from NumberToString import NumberToStringMachine
from pkg_resources import resource_string

class NumberToStringTests(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("NumberToStringTests")
        self.locale = 'en_US'
        self.testcases = resource_string(__name__, self.locale + '.testcases') 
        self.translator = NumberToStringMachine(self.locale)
        #self.logger.debug(self.testcases)

    def tearDown(self):
        pass

    def test_locale(self):
        for testcase in self.testcases.splitlines():
            self.logger.debug(testcase)
            testcase = testcase.strip()
            if testcase.startswith('#'):
                continue
            (test_name, number_str, answer) = shlex.split(testcase)
            #self.logger.debug("test_name = %s, number_str = %s, answer= % s" % (test_name, number_str, answer))
            test_translation = self.translator.translate(int(number_str))
            self.logger.debug(test_translation)
            self.assertEqual(test_translation, answer, 
                             msg="%s (%s)\n\tExpected: '%s'\n\tReceived: '%s'\n" % 
                                 (test_name, self.locale, answer, test_translation))

def main(locale='en_US'):
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("NumberToStringTests").setLevel(logging.DEBUG)
    unittest.main()

if __name__ == '__main__':
    main()
