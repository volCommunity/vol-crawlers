import json
from urllib.parse import urljoin

import scrapy

from ..items import JobItem, OrganisationItem

SITE_NAME = "Do It"
SITE_URL = "https://do-it.org"
API_URL = "https://api.do-it.org"
COUNTRY = "UK"


class DoItSpider(scrapy.Spider):
    name = "do-it.org"
    allowed_domains = ["api.do-it.org"]
    start_urls = (
        # Site is rendered on client site, consume the API directly
        urljoin(API_URL, 'v2/opportunities'),
    )
    # Tell the API to return JSON instead the default (XML)
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {'Content-Type': 'application/json'}
    }

    def parse(self, response):
        """
        Example https://api.do-it.org/v2/opportunities

        :param response:
        :return: Scrapy Request generators
        """

        json_response = json.loads(response.body_as_unicode())

        for job in json_response['data']['items']:
            yield self.parse_job_page(job)

        try:
            next_page_url = json_response['links']['next']['href']
            if next_page_url is not None:
                yield scrapy.Request(response.urljoin(next_page_url))
        except KeyError:
            pass

    def parse_job_page(self, job):
        """
        Parse a job and yield it for a pipeline to create.
        :param job:
        :return a JobItem generator:
        """

        # Default values should be handled a little better,
        # see https://github.com/volCommunity/vol-crawlers/issues/24
        try:
            city = job['locations'][0]['city']
        except IndexError:
            pass

        if city is None:
            city = "Unknown"

        job_item = JobItem(
            title=job['title'],
            text=job['description'],
            country=COUNTRY,
            labels=[label['name'] for label in job['interests']],
            city=city,  # TODO: support multiple locations
            sites=[SITE_NAME],
            site_name=SITE_NAME,
            site_url=SITE_URL,
            region="placeholder",
            organisation=job['owner_recruiter']['name'],
            # TODO: Chose to save the url to the org in the API, however we do already have and could save us the extra
            # requests. Possible item for improvement.
            # organisation_url=job['owner_recruiter']['website'], # Org own URL
            organisation_url=job['owner_recruiter']['links'][0]['href'],  # Hope there is one TODO: try
            # The job id, will look like so https://do-it.org/#/opportunities/295754a4-8bbd-47c7-acac-3280d7ee75ca
            url=urljoin(SITE_URL, "/#/opportunities/{}".format(job['id'])),
            api_url=API_URL,
        )

        return job_item

    def parse_org_page(self, response):
        """
        Parse an organisation page and return an Organisation item. This will be utilised when creating jobs
        from a pipeline.

        Example: https://api.do-it.org/v2/orgs/volunteering-gloucestershire

        Note that we may have all the data for the org in the original response! Dont' think extra
        call are needed.

        :param response:
        :return SeekOrganisationItem:
        """

        json_response = json.loads(response.body_as_unicode())
        r = json_response['data']['recruiter']

        # Default values should be handled a little better,
        # see https://github.com/volCommunity/vol-crawlers/issues/24
        if r['city'] is None:
            r['city'] = "Unknown"

        # If they do not have have their own site, use the one from our source
        if r['website'] is None:
            r['website'] = urljoin(SITE_URL, "/#/organisations/{}".format(r['id']))

        # Default values should be handled a little better,
        # see https://github.com/volCommunity/vol-crawlers/issues/24
        if r['blurb'] is None:
            r['blurb'] = "This organisation does not yet have a description."

        org = OrganisationItem(
            name=r['name'],
            url=r['website'],
            description=r['blurb'],
            city=r['city'],
            country=COUNTRY,
            region="placeholder",
        )

        return org
