#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2


class BingSearchEngine(object):
    def search(self, query, advanced_operators):
        """Function that query Bing API."""
        key = 'wP54IdS2ze1pwf2z+v9iOMGK3z3DDDvCKQYH/I9rtHA='
        query = urllib2.quote(query)
        if advanced_operators != '':
            advanced_operators = urllib2.quote(advanced_operators)

        # create credential for authentication
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; \
            Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
        credentials = (':%s' % key).encode('base64')[:-1]
        auth = 'Basic %s' % credentials
        url = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/Web' + \
              '?Query=%27' + query + '%20' + advanced_operators + \
              '%27&$top=10&$format=json'

        request = urllib2.Request(url)
        request.add_header('Authorization', auth)
        request.add_header('User-Agent', user_agent)
        request_opener = urllib2.build_opener()

        # TODO use this information with logger
        print "INFO: Query - %s" % url

        response = request_opener.open(request)
        response_data = response.read()
        json_result = json.loads(response_data)

        result_list = json_result['d']['results']
        return result_list


def main():
    query = "NANODEVICE Novel Concepts, Methods, and Technologies for the Production of Portable, Easy-to-Use Devices for the Measurement and Analysis of Airborne Engineered Nanoparticles in Workplace Air -site:cordis.europa.eu"
    engine = BingSearchEngine()
    print engine.search(query, '')

if __name__ == "__main__":
    main()
