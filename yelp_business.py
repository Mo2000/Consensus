#!/usr/bin/env python3.4
"""
Yelp API v2.0 code sample.

This program demonstrates the capability of the Yelp API version 2.0
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/documentation for the API
documentation.

This program requires the Python oauth2 library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
import argparse
import json
import pprint
import urllib.parse
import urllib.request
import urllib.error

import oauth2


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'pizza'
DEFAULT_BUSINESS_ID = 'savas-philadelphia'
DEFAULT_LOCATION = 'Philadelphia, PA'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'jRsOYLxrrJfI8PerXqG_-w'
CONSUMER_SECRET = 'pXVdi4ZDPYwyzvTxJJWaPt0R9xo'
TOKEN = 'UHnq4pncP7gPOQoMtisxyYFM_jdUGhQs'
TOKEN_SECRET = 'ogyGas7GV04NQ6qdQy-rJD2k9k4'


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.parse.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    #print(u'Querying {0} ...'.format(url))

    conn = urllib.request.urlopen(signed_url, None)
    try:
        str_response = conn.readall().decode('utf-8')
        response = json.loads(str_response)
    finally:
        conn.close()

    return response


def search(term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location)

    businesses = response.get('businesses')

    if not businesses:
        #print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    #print(u'{0} businesses found, querying business info ' \
    #    'for the top result "{1}" ...'.format(
    #        len(businesses), business_id))
    response = get_business(business_id)

    #print(u'Result for business "{0}" found:'.format(business_id))
    #pprint.pprint(response, indent=2)


def get_categories(business_id):
    """Given a Yelp business ID, return a set containing the categories of the
    business"""
    l = get_business(business_id)['categories']
    s = set()
    for l1 in l:
        s |= set(l1)
    return s


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')
    parser.add_argument('-b', '--business', dest='business_id', default=DEFAULT_BUSINESS_ID,
                        type=str, help='Search term (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except urllib.error.HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    import sys
    get_categories(sys.argv[1])
    #main()
