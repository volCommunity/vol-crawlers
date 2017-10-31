from urllib.parse import urljoin

import requests
import scrapy

from ..items import JobItem, OrganisationItem

SITE_NAME = "Charity Job"
SITE_URL = "https://www.charityjob.co.uk"
COUNTRY = "UK"


class SeekSpider(scrapy.Spider):
    name = "charityjob.co.uk"
    allowed_domains = ["www.charityjob.co.uk"]
    start_urls = (
        'https://www.charityjob.co.uk/volunteer-jobs',
    )

    def __init__(self, rest_url='', *args, **kwargs):
        super(SeekSpider, self).__init__(*args, **kwargs)
        self.rest_url = rest_url

    def parse(self, response):
        """
        :param response:
        :return: Scrapy Request generators
        """
        job_urls = response.xpath('//div[@class="title"]/h3/a/@href').extract()
        for job_url in job_urls:
            # Until we support updates (https://github.com/volCommunity/vol-crawlers/issues/26)
            # skip jobs urls for which we already have objects.
            if requests.get(urljoin(self.rest_url, 'api/jobs'),
                            params={'url': job_url}).json()['count'] == 0:
                yield scrapy.Request(response.urljoin(job_url), callback=self.parse_job_page)
            else:
                print("Skipping previously visited job %s" % job_url)

        next_page_url = response.css('a.next::attr(href)').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_job_page(self, response):
        """
        Parse a job and yield it for a pipeline to create.
        :param response:
        :return a SeekJobItem generator:
        """

        job = JobItem(
            title=response.xpath(
                '//article[@class="job-advert with-border"]/header/div[@class="title"]/h1/text()').extract_first(),
            url=response.url,
            text="\n".join(
                response.xpath(
                    '//article[@class="job-advert with-border"]/div[@class="page-text clear-fix"]/p/text()').extract()),
            labels=response.xpath('//td/span/a/text()').extract(),
            # TODO: surely we can do better than this
            city=response.xpath('//table[@class="list-with-icons"]/tbody/tr/td/text()').extract()[5],
            sites=[SITE_NAME],
            region="placeholder",
            country=COUNTRY,
            organisation=response.xpath('//p[@class="post-by sub-text"]/a/text()').extract_first(),
            organisation_url=response.xpath('//p[@class="post-by sub-text"]/a/@href').extract_first(),
            site_name=SITE_NAME,
            site_url=SITE_URL,
        )

        yield job

    def parse_org_page(self, response):
        """
        Parse an organisation page and return an Organisation item. This will be utilised when creating jobs
        from a pipeline.
        :param response:
        :return SeekOrganisationItem:
        """

        org = OrganisationItem(
            name=response.xpath('//div[@class="header recruiter-jobs-header"]/h2/span/text()').extract_first(),
            url=response.url,
            description="\n".join(response.xpath('//section[@class="profile-info"]/p').extract()),
            city=response.xpath('//li[@class="location"]/text()').extract_first(),
            region="placeholder",
            # TODO: add tags too!?
            country=COUNTRY,
        )

        return org
