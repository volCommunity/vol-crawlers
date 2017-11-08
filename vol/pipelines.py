# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from urllib.parse import urljoin

import requests
from scrapy.exceptions import DropItem
from scrapy.http import HtmlResponse
from scrapy.utils.serialize import ScrapyJSONEncoder


class BasePipeline(object):
    """

    """

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
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


class DuplicatesPipeline(BasePipeline):
    def process_item(self, item, spider):
        """
        Check if an item  already exists. Raise DropItem if does, which will
        prevent  the item from being processed further.

        :param item:
        :param spider:
        :raise DropItem:
        :return item:
        """
        self.headers['Authorization'] = 'Token {}'.format(spider.rest_token)

        payload = {'url': item['url']}
        r = requests.get(urljoin(spider.rest_url, 'api/jobs'),
                         params=payload,
                         headers=self.headers)
        j = r.json()
        if j['count'] != 0:
            raise DropItem("Job with url %s already exists, skipping" % item['url'])

        return item


class DependenciesPipeline(BasePipeline):
    def process_item(self, item, spider):
        """
        Process dependencies of items. At the moment these are a site, labels and organisations.
        If dependencies are not yet there, we will create them. If they are, fetch and store the IDs.

        :param item:
        :param spider:
        :return item:
        """

        self.headers['Authorization'] = 'Token {}'.format(spider.rest_token)
        # Organisation

        # Does it exist? If so, skip parsing the org page and store our ID, assuming our API will be faster
        # than the target site.
        r = requests.get(urljoin(spider.rest_url, 'api/organisations'),
                         params={'name': item['organisation']},
                         # What the hell was the reason for this again!?
                         # params={'name': "{} | SEEK Volunteer".format(item['organisation'])},
                         headers=self.headers)
        j = r.json()
        if j['count'] > 0:
            # Done
            item['organisation'] = j['results'][0]
            return item

        if item['organisation_url'] is not None:
            # If org was not created yet, parse the page, populate item and let job creation do the
            # work in one swoop
            #
            #
            # Warning, hack alert, see https://stackoverflow.com/a/45810801/4372104
            #
            # We should probably parse the organisation page using a proper spider,
            # but we have no desire to get all organisations, just the ones our
            # jobs depend on.
            # Hence we get the organisation page using requests, convert it into HtmlResponse
            # so that we are able to call xpath on it, and move on.

            url = urljoin(item['site_url'], item['organisation_url'])

            # If we have an API to talk to, use it
            if 'api_url' in item and item['api_url'] is not None:
                url = urljoin(item['api_url'], item['organisation_url'])

            r = requests.get(url)
            resp = HtmlResponse(body=r.content, url=url)
            org = spider.parse_org_page(resp)

            item['organisation'] = self._item_to_json(org)

        return item


class CreateJobPipeline(BasePipeline):
    def process_item(self, item, spider):
        """
        Create a job
        :param item:
        :param spider:
        :raise DropItem:
        :return item:
        """
        item['labels'] = [{"name": label} for label in item['labels']]
        item['sites'] = [{"name": item['site_name'], "url": item['site_url']}]

        print("going to create item: %s" % item)
        self.headers['Authorization'] = 'Token {}'.format(spider.rest_token)
        data = self._item_to_json(item)

        print("going to create item: %s" % data)

        r = requests.post(urljoin(spider.rest_url, 'api/jobs'),
                          json=data,
                          headers=self.headers)

        if r.status_code != 201:
            j = r.json()
            raise DropItem("Failed to create job. Response code: {} with contents: {}".format(r.status_code, j))

        return item
