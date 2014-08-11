""" NumberToString.py
Converts a number to an English String.  For example:

> number-to-string 120
> one hundred twenty

Constraints:
    - number is base 10
    - number can be negative

Basic algorithm

# 1. Build hash tables
# 1. Parse Command-line arguments, store input number into 'number' var
# 2. Determine sign of number
# 3. Use the Math.log function to determine how large the number is (# of digits)
"""

import gettext
import math
import sys

# I don't feel like translating beyond the decillion range, so setting an arbitrary limit
NUMBER_MAX = 100000000000000000000000000000000000

class NumberToStringMachine(object):


    def __init__(self, locale='en_US'):
        self.module_name = 'NumberToString'
        self.load_locale(locale)
    # END __init__()


    def load_locale(self, locale):
        """ load_locale()
        """
        kwargs = {}
        if locale:
            kwargs['languages'] = [locale]
        translations = gettext.translation(self.module_name, **kwargs)
        self.setup_message_hashes(translations)
    # END load_locale()
        

    def setup_message_hashes(self, translations):
        _ = translations.ugettext
        self.messages = {
            'magnitudes' : {
                 0 : '',                  3 : _('thousand'),    6 : _('million'),
                 9 : _('billion'),       12 : _('trillion'),   15 : _('quadrillion'),
                 18 : _('quintillion'),  21 : _('sextillion'), 24 : _('septillion'),
                 27 : _('octillion'),    30 : _('nonillion'),  33 : _('decillion'),
            },
            'cardinals' : {
                 1 : _('one'),        2 : _('two'),       3 : _('three'),     4 : _('four'),     
                 5 : _('five'),       6 : _('six'),       7 : _('seven'),     8 : _('eight'),    
                 9 : _('nine'),      10 : _('ten'),      11 : _('eleven'),   12 : _('twelve'),  
                13 : _('thirteen'),  14 : _('fourteen'), 15 : _('fifteen'),  16 : _('sixteen'), 
                17 : _('seventeen'), 18 : _('eighteen'), 19 : _('nineteen'), 20 : _('twenty'),  
                30 : _('thirty'),    40 : _('forty'),    50 : _('fifty'),    60 : _('sixty'),   
                70 : _('seventy'),   80 : _('eighty'),   90 : _('ninety'),  100 : _('hundred'),
            },
            # Ideally, we'd grab much of this data directly from the locale itself, but std python 
            # doesn't have a way to load non-message locale data without setting the locale
            # for the entire program.  The downside of this approach is that the "C" locale
            # will no longer work properly.
            'locale_data' : {
                # grouping: How many orders of magnitude are in a group. For example, in English
                #           numbers are grouped every 3 orders of magnitude. NOTE: this is a 
                #           slight simplification - in some languages like Hindi, the grouping
                #           changes as the numbers progress.  If we decide to support such 
                #           languages, this will need to be modified to mirror the approach
                #           taken by the LC_NUMERIC 'grouping' key.
                #           Example: "twenty-five million, thirty-six thousand, two hundred and seven."
                'grouping' : _('grouping'),
                # group_sep: The separator between groupings.
                #           Example: "two thousand, seven hundred"  -> ", "
                'group_sep' : _('group_sep'),
                # hundreds_sep: The separator between the cardinal number and the word for 'hundred'.
                #           Example: "seven hundred" -> " "
                'hundreds_sep' : _('hundreds_sep'),
                # hundreds_tens_sep: The separator between the hundreds and tens place.
                #           Example: "seven hundred and twenty-six" -> " and "
                'hundreds_tens_sep' : _('hundreds_tens_sep'),
                # tens_ones_sep: The separator between the tens and ones place.
                #           Example: "twenty-six" -> "-"
                'tens_ones_sep' : _('tens_ones_sep'),
                # cardinal_magnitude_sep: Separator between the cardinality of the group and its magnitude.
                #           Example: "twenty-six million" -> " "
                'cardinal_magnitude_sep' : _('cardinal_magnitude_sep'),
                # negative: The indicator for a negative number
                'negative' : _('negative'),
                # Where the negative indicator is inserted in the string. Possible values:
                #           'beginning'
                #           'end' 
                'n_sign_posn' : _('n_sign_posn'),
                # positive: The indicator for a positive number
                'positive' : _('positive'),
                # Where the negative indicator is inserted in the string:
                #           'beginning'
                #           'end' 
                'p_sign_posn' : _('p_sign_posn'),
                # How to terminate the sentence.
                #           Example: "." in English 
                'sentence_termination' : _('sentence_termination'),
                # Special case: zero
                'zero' : _('zero'),
            }
        }
        self.log_group_size = int(self.messages['locale_data']['grouping'])
        self.dec_group_size = 10 ** self.log_group_size
    # END setup_message_hashes()


    def translate_group(self, number):
        """ translate_group(number)
            @param int number: the number to be translated
            @return string: the natural language translation of that number

        Given a number less than 1000, this function translates that number using the 
        following algorithm:

            1. Find the number of 100s
        """
        group_translation = ""
        number_of_hundreds = number / 100
        if (number_of_hundreds):
            group_translation = self.messages['cardinals'][number_of_hundreds] + \
                                self.messages['locale_data']['hundreds_sep'] + \
                                self.messages['cardinals'][100]
        remainder  = number % 100
        if remainder != 0:
            if (number_of_hundreds):
                group_translation += self.messages['locale_data']['hundreds_tens_sep']
            if remainder in self.messages['cardinals']:
                group_translation += self.messages['cardinals'][remainder]
            else:
                tens = remainder / 10
                group_translation += self.messages['cardinals'][10 * tens] + \
                                     self.messages['locale_data']['tens_ones_sep']
                ones = remainder % 10
                group_translation += self.messages['cardinals'][ones]
        return group_translation
    # END translate_group()


    def translate(self, number):
        """ translate(number)
            @param number: the number to translate
            @return string: the translated number

        Build a translated string

        1. Special case - Zero
        2. Determine sign of the number
         Add sign indicator
         Add sentence terminator
        """
        result = ""

        # 1. Special case - Zero

        # 2. Determine sign of number
        if (number < 0):
            negative = True
            number = abs(number)
        else:
            negative = False

        # 5. Iterate over each numeric group, building a list of sub-translations that will be 
        #    combined together at the end for the full translation.
        groups = [] 
        current_group = 0
        while number > 0:
            group_translation = self.translate_group(number % self.dec_group_size)     
            if self.messages['magnitudes'][current_group]:
                group_translation += self.messages['locale_data']['cardinal_magnitude_sep'] + \
                                     self.messages['magnitudes'][current_group]
            groups.insert(0, group_translation)
            number /= self.dec_group_size
            current_group += self.log_group_size
        full_translation = self.messages['locale_data']['group_sep'].join(groups)

        # Add sign indicator
        if (negative):
            if self.messages['locale_data']['n_sign_posn'] == 'beginning':
                full_translation = self.messages['locale_data']['negative'] + full_translation
            elif self.messages['locale_data']['n_sign_posn'] == 'end': 
                full_translation += self.messages['locale_data']['negative']
        else:
            if self.messages['locale_data']['p_sign_posn'] == 'beginning':
                full_translation = self.messages['locale_data']['positive'] + full_translation
            elif self.messages['locale_data']['p_sign_posn'] == 'end':
                full_translation += self.messages['locale_data']['positive']

        # Add sentence terminator
        full_translation += self.messages['locale_data']['sentence_termination']

        return full_translation
    # END translate()
