""" app.py - NumberToStringAPI - A REST API for translating numbers
"""
# Python Stdlib

# 3rd Party Modules
from flask import Flask

import NumberToStringAPI

# MAIN()
if __name__ == '__main__':
    flask = Flask(__name__)
    try:
        api = NumberToStringAPI.NumberToStringAPI(flask)
        api.loadRoutes()
        flask.run(host='0.0.0.0', debug = True)
    except Exception as e:
        print "Encountered unexpected Exception %r" % e
        exit(-1)
