#!/usr/bin/env python

from __future__ import print_function

import logging

from os import path, makedirs, listdir
from StringIO import StringIO
from re import sub

# External modules.
from lxml import etree
from requests import get

logger = logging.getLogger()

class WorldBankAPIXML:
    '''
    The World Bank API:
    * Returns a status of 200 if a requested page is out of range
    * Does not provide a next link etc.
    '''
    def __init__(self, endpoint):
        self.base_url = 'http://api.worldbank.org'
        self.endpoint = '/'.join([self.base_url, endpoint])
        self.payload = { 'format': 'xml', 'page': 1, 'per_page': 100 }
        self.pages = 0

    def get_page(self, page):
        self.payload['page'] = page
        res = get(self.endpoint, params=self.payload)
        return res.content

    def get_pages(self, content):
        tree = etree.fromstring(content)
        pages = tree.get('pages')
        return int(pages)

    def list(self):
        content = self.get_page(1)
        self.pages = self.get_pages(content)
        return content if self.pages > 0 else None

    def list_next(self):
        next_page = self.payload['page'] + 1
        return self.get_page(next_page) if next_page <= self.pages else None

class CountriesEndpoint:
    '''The World Bank API: Countries Endpoint'''
    def __init__(self):
        self.endpoint = 'countries'
        self.tag = '{http://www.worldbank.org}country'
        self.ns = {'wb': 'http://www.worldbank.org'}

    def get_context(self, xml):
        io = StringIO(xml)
        return etree.iterparse(io, events=('end',), tag=self.tag)

    def get_region(self, element):
        return element.find('wb:region', namespaces=self.ns).attrib['id']

    def get_name(self, element):
        return element.find('wb:name', namespaces=self.ns).text

    def get_id(self, element):
        return element.attrib['id']

    def get_country(self, element):
        country = []
        if self.get_region(element) != 'NA':
            # A "country" with a region of NA is itself a region.
            country.append(self.get_id(element))
            country.append(self.get_name(element))
        return country

    def list_all(self, **kwargs):
        wb = WorldBankAPIXML(self.endpoint)
        content = wb.list()
        while content:
            context = self.get_context(content)
            for event, element in context:
                country = self.get_country(element)
                if country:
                    yield country
            content = wb.list_next()

def setup():
    if not path.exists('tmp'):
        makedirs('tmp')
    if not path.exists('data'):
        makedirs('data')

def safe_filename(string):
    return ''.join([c for c in string if c.isalpha()]).lower()

def retrieve_indicator(id, name, indicator):
    '''
    Retrieve and save indicator XML files
    1. Build an endpoint string from an ISO-3 code and indicator
    2. Retrieve the XML data
    3. Build a filename string from a country name
    4. Save the XML data to a file
    '''
    endpoint = '/'.join(['countries', id, 'indicators', indicator])
    wb = WorldBankAPIXML(endpoint)
    content = wb.get_page(1)
    filename = safe_filename(name) + '.xml'
    dest = path.join('tmp', filename)
    with open(dest, 'wb') as file:
        logger.info("Writing {filename}".format(filename=filename))
        file.write(content)

def retrieve():
    '''
    Retrieve our data from the World Bank API
    1. Retrieve ISO-3 codes and country names
    2. Retrieve and save indicator XML files
    '''
    indicator = 'pa.nus.ppp'
    for id, name in CountriesEndpoint().list_all():
        retrieve_indicator(id, name, indicator)

def xml_to_csv():
    '''
    Transform all the XML files in a directory to CSV-like strings.
    '''
    xslt = path.join('scripts/xslt', 'pa-nus-ppp.xslt')
    xslt_root = etree.parse(xslt)
    transform = etree.XSLT(xslt_root)
    for filename in listdir('tmp'):
        if filename.endswith('.xml'):
            xml = path.join('tmp', filename)
            doc = etree.parse(xml)
            result_tree = transform(doc)
            yield unicode(result_tree)

def extract():
    '''
    Extract data from the source data files in `./tmp` and write to `./data`
    '''
    filename = 'ppp-gdp.csv'
    dest = path.join('data', filename)
    header = 'Country,Country ID,Year,PPP'
    with open(dest, 'wb') as file:
        logger.info("Writing {filename}".format(filename=filename))
        print(header, file=file)
        for data in xml_to_csv():
            file.write(data)

def process():
    setup()
    retrieve()
    extract()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    process()
