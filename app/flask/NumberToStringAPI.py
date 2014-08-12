""" routes.py - NumberToStringApi - A REST API for translating numbers to strings
"""

# Python stdlib
import ConfigParser
import json
import logging
import pprint as pp
import sys

# 3rd Party Modules
from flask import request
from flask import abort

# Codero Modules
import NumberToString
from NumberToString.tests.NumberToStringTests import list_installed_locales

class NumberToStringAPI():
    """ class NumberToStringAPI
    Methods:
        __init__() - constructor
            - loads config values, sets up logging, loads the RackTables module
        loadRoutes()
            - Iterates over the routes table, adding each route to the flask context.
    """

    # Routes
    routes = {
        'translation/<locale>/<int:number>' : {
            'methods' : ['GET'],
            'function' : 'get_translation',
        },
    }
    # END routes

    def __init__(self, flask, config_file='NumberToStringAPI.config'):
        """ __init__ - NumberToStringAPI constructor
        1. Save flask context - self.flask
        2. load config file - config values saved to self.config dictionary
        3. Set up logging - self.LOGGER
        4. load NumberToString module - self.machine
        """
        # 1. Save flask context
        self.flask = flask

        # 2. Load Config
        conf_parser = ConfigParser.SafeConfigParser()
        conf_parser.read(config_file)
        self.config = dict(conf_parser.items('NumberToString'))

        # 3. Set up logger
        logging.basicConfig(stream=sys.stderr, 
                            format='%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
        logging.getLogger("NumberToStringAPI").setLevel(logging.INFO)
        self.LOGGER = logging.getLogger("NumberToStringAPI")
        try:
            self.LOGGER.info("START NumberToStringAPI")
        except Exception as e:
            sys.stderr.write("Fatal Error: Could not instantiate LOGGER\n")
            raise

        # 4. Load a machine for each available locale
        self.config['locales'] = list_installed_locales()
        self.machines = {}
        for locale in self.config['locales']:
            self.machines[locale] = NumberToString.NumberToStringMachine(locale=locale)


    # END __init__()


    def loadRoutes(self):
        """ loadRoutes() - Iterate over the routes table, adding each route to the flask context.
        """
        self.LOGGER.info("Entered loadRoutes")
        api_route_prefix = '/%s/%s/' % (self.config['api_name'], self.config['api_version'])
        for route, attributes in self.routes.items():
            self.flask.add_url_rule(api_route_prefix + route,
                                    attributes['function'],
                                    getattr(self, attributes['function']),
                                    methods=attributes['methods'])
    # END loadRoutes()


    def get_translation(self, locale, number):
        """
        GET variables:
            string locale: locale to translate to, e.g. en_US
            int number: the number to translate

        @return Dict mixed: a json-formatted dictionary containing status and the result

        """
        self.LOGGER.info("Entered get_translation")
        # 1. Validate input parameters
        pretty=False
        try:
            if 'pretty' in request.args:
                pretty = request.args['pretty']
        except KeyError as e:
            self.LOGGER.error("%r" % e)
            abort(400)
        if pretty and pretty == 'true':
            pretty_print = {'sort_keys' : True,
                            'indent'    : 4,
            }
            pretty_print_html_begin = '<pre>'
            pretty_print_html_end = '</pre>'
        else:
            pretty_print = {}
            pretty_print_html_begin = ""
            pretty_print_html_end = ""

        try:
            result = self.machines[locale].translate(number)
            status = 'SUCCESS'
        except KeyError as e:
            self.LOGGER.error("%r", e)
            result = "invalid locale"
            status = 'FAILURE'
        except OverflowError as e:
            self.LOGGER.error("%r", e)
            result = "OverflowError: %d is too large to translate"
            status = 'FAILURE'
        except Exception as e:
            self.LOGGER.error("%r", e)
            result = "UNKNOWN ERROR: %r" % e
            status = 'FAILURE'

        return pretty_print_html_begin + \
               json.dumps({ 'status' : status,
                            'result' : result,
                          }, **pretty_print
               ) + \
               pretty_print_html_end
    # END get_addresses()


# END class NumberToStringAPI
