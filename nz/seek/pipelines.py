# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
from urllib.parse import urljoin

import requests
from scrapy.exceptions import DropItem
from scrapy.http import HtmlResponse
from scrapy.utils.serialize import ScrapyJSONEncoder

from .items import SeekSiteItem
from .spiders.seek import SITE_URL, SITE_NAME


class SeekBasePipeline(object):
    """

    """

    def __init__(self):
        token = os.environ.get('REST_TOKEN', False)
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Token {}'.format(token)}
        self.rest_base_url = os.environ.get('REST_URL', False)
        self._encoder = ScrapyJSONEncoder()

    def _item_to_json(self, obj):
        """
        Utility that takes a object, serializes it using ScrapyJSONEncoder
        and returns a deserialized version of the data.

        We use this to convert Scrapy models to JSON objects we can to requests.

        :param obj:
        :return dict:
        """
        return json.loads(self._encoder.encode(obj))


class SeekDuplicatesPipeline(SeekBasePipeline):
    def process_item(self, item, spider):
        """
        Check if an item  already exists. Raise DropItem if does, which will
        prevent  the item from being processed further.

        :param item:
        :param spider:
        :raise DropItem:
        :return item:
        """

        payload = {'title': item['title']}
        r = requests.get(urljoin(self.rest_base_url, 'api/jobs'),
                         params=payload,
                         headers=self.headers)
        j = r.json()

        print("JSON: {}".format(j))
        if j['count'] != 0:
            print("Already there, skipping")
            raise DropItem("Job already exists, skipping")

        return item


class SeekDependenciesPipeline(SeekBasePipeline):
    def process_item(self, item, spider):
        """
        Process dependencies of items. At the moment these are a site, labels and organisations.
        If dependencies are not yet there, we will create them. If they are, fetch and store the IDs.

        :param item:
        :param spider:
        :return item:
        """

        # TODO: split items out in different pipelines or methods.
        # Labels
        tmp = []
        for l in item['labels']:
            r = requests.get(urljoin(self.rest_base_url, 'api/labels'),
                             params={'name': l},
                             headers=self.headers)
            j = r.json()
            if j['count'] > 0:
                tmp.append(j['results'][0]['id'])
            else:
                r = requests.post(urljoin(self.rest_base_url, 'api/labels'),
                                  json={'name': l},
                                  headers=self.headers)
                j = r.json()
                tmp.append(j['id'])

        item['labels'] = tmp

        # Organisation
        r = requests.get(urljoin(self.rest_base_url, 'api/organisations'),
                         params={'name': "{} | SEEK Volunteer".format(item['organisation'])},
                         headers=self.headers)
        j = r.json()
        print("looked for org {} and got: {}".format(item['organisation'], j))
        if j['count'] > 0:
            item['organisation_id'] = j['results'][0]['id']
        else:
            # Warning, hack alert, see https://stackoverflow.com/a/45810801/4372104
            #
            # We should probably parse the organisation page using a proper spider,
            # but we have no desire to get all organisations, just the ones our
            # jobs depend on.
            # Hence we get the organisation page using requests, convert it into HtmlResponse
            # so that we are able to call xpath on it, and move on.
            url = urljoin(SITE_URL, item['organisation_url'])
            r = requests.get(url)
            resp = HtmlResponse(body=r.content, url=url)
            org = spider.parse_org_page(resp)

            data = self._item_to_json(org)
            r = requests.post(urljoin(self.rest_base_url, 'api/organisations'),
                              json=data,
                              headers=self.headers)
            j = r.json()

            item['organisation_id'] = (j['id'])

        # Sites
        tmp = []
        for i in item['sites']:
            r = requests.get(urljoin(self.rest_base_url, 'api/sites'),
                             params={'name': i},
                             headers=self.headers)
            j = r.json()
            if j['count'] > 0:
                tmp.append(j['results'][0]['id'])
            else:
                site = SeekSiteItem(name=SITE_NAME,
                                    url=SITE_URL)
                r = requests.post(urljoin(self.rest_base_url, 'api/sites'),
                                  json=site,
                                  headers=self.headers)
                j = r.json()
                tmp.append(j['id'])

        item['sites'] = tmp

        return item


class SeekCreateJobPipeline(SeekBasePipeline):
    def process_item(self, item, spider):
        """
        Create a job
        :param item:
        :param spider:
        :raise DropItem:
        :return item:
        """

        data = self._item_to_json(item)

        r = requests.post(urljoin(self.rest_base_url, 'api/jobs'),
                          json=data,
                          headers=self.headers)

        if r.status_code != 201:
            j = r.json()
            raise DropItem("Failed to create job. Response code: {} with contents: {}".format(r.status_code, j))

        return item
