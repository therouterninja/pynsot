# -*- coding: utf-8 -*-

"""
pynsot.py - Simple Python API client for NSoT REST API
"""

__author__ = 'Jathan McCollum'
__maintainer__ = 'Jathan McCollum'
__email__ = 'jathan@dropbox.com'
__copyright__ = 'Copyright 2014 Dropbox'
__version__ = '0.1'


import slumber


AUTH_HEADER = 'X-NSoT-Email'


class API(slumber.API):
    """
    Magic REST API client for NSoT.
    """
    def __init__(self, *args, **kwargs):
        kwargs.pop('auth', None) # Ditch default auth
        email = kwargs.pop('email', None)
        auth_header = kwargs.pop('auth_header', AUTH_HEADER)

        super(API, self).__init__(*args, **kwargs)

        # Hard-code disable trailing slash
        self._store['append_slash'] = False # No slashes!

        # If email is provided, use this to set auth header
        if email is not None:
            self.auth(email=email)

        self._auth_header = auth_header

    def auth(self, *args, **kwargs):
        """Set the auth header."""
        email = kwargs.get('email')
        if email is None:
            raise RuntimeError('You must provide an email!')
        s = self._store['session']
        s.headers.update({self._auth_header: email})

if __name__ == '__main__':
    #url = 'http://localhost:8888/api'
    import json

    url = 'http://localhost:8990/api'
    email = 'jathan@localhost'
    api = API(url)
    api.auth(email=email)

    print 'GET /sites'
    print json.dumps(api.sites().get(), indent=4)
    print

    print 'GET /sites/1/networks'
    print json.dumps(api.sites(1).networks.get(), indent=4)
    print

    print 'GET /sites/1/network_attributes'
    print json.dumps(api.sites(1).network_attributes.get(), indent=4)
    print
