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

    def parse(self, response):
        """
        :param response:
        :return: Scrapy Request generators
        """
        job_urls = response.xpath('//div[@class="title"]/h3/a/@href').extract()
        for job_url in job_urls:
            yield scrapy.Request(response.urljoin(job_url), callback=self.parse_job_page)

        next_page_url = response.css('a.next::attr(href)').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_job_page(self, response):
        """
        Parse a job and yield it for a pipeline to create.
        :param response:
        :return a SeekJobItem generator:
        """

        # TODO: implement this
        job = JobItem(
            title=response.xpath('/html/head/meta[contains(@property, "og:title")]/@content').extract_first(),
            url=response.xpath('/html/head/meta[contains(@property, "og:url")]/@content').extract_first(),
            text="\n".join(response.xpath('//div[@id="opp-desc"]/p/text()').extract()),
            labels="",
            city="",
            sites=[SITE_NAME],
            region="placeholder",
            country=COUNTRY,
            organisation=response.xpath('//p[@class="byline"]/strong/a/text()').extract_first(),
            organisation_url=response.xpath('//p[@class="byline"]/strong/a/@href').extract_first(),
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

        # TODO: implement this
        org = OrganisationItem(
            name=response.xpath('/html/head/meta[contains(@property, "og:title")]/@content').extract_first(),
            url=response.xpath('/html/head/meta[contains(@property, "og:url")]/@content').extract_first(),
            description=response.xpath('//div[@id="org-desc"]/p/text()').extract_first(),
            city=response.xpath('//div[@class="snapshot"]/p/span/text()').extract_first(),
            region="placeholder",
            # TODO: add tags too!?
            country=COUNTRY,
        )

        return org
