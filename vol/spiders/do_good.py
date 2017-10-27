import scrapy

from ..items import JobItem

SITE_NAME = "Do Good Jobs"
SITE_URL = "https://dogoodjobs.co.nz"
COUNTRY = "NZ"


class DoGoodSpider(scrapy.Spider):
    name = "dogoodjobs.co.nz"
    allowed_domains = ["dogoodjobs.co.nz"]
    start_urls = (
        'https://dogoodjobs.co.nz/volunteer-jobs',
    )

    def parse(self, response):
        """
        :param response:
        :return: Scrapy Request generators
        """
        job_urls = response.css("#content #mainContent ol li a::attr(href)").extract()
        for job_url in job_urls:
            yield scrapy.Request(response.urljoin(job_url), callback=self.parse_job_page)

        next_page_url = response.css("#content #mainContent a.next::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_job_page(self, response):
        """
        Parse a job and yield it for a pipeline to create.
        :param response:
        :return a SeekJobItem generator:
        """

        job = JobItem(
            title=response.xpath('/html/head/meta[contains(@property, "og:title")]/@content').extract_first(),
            url=response.url,
            text="\n".join(response.xpath('//div[@class="section_content"]/p/text()').extract()),

            # Treat the category as label
            labels=[response.xpath('//p[@class="meta"]/em/a/text()').extract_first()],
            city=response.xpath('//strong[@class="job-location"]/text()').extract_first(),
            sites=[SITE_NAME],
            region="placeholder",
            country=COUNTRY,
            # TODO: This could  be a little tidier. If this offends you, please improve
            # Stripping of the newlines like so, still leaves us with a trailing newline and dash:
            # >>> response.xpath('//p[@class="meta"]/text()').extract_first().strip('\n')
            # 'GirlGuiding New Zealand\n–'
            # doing an rstrip('\n-') does not remove it and I need to move on.
            organisation=response.xpath('//p[@class="meta"]/text()').extract_first().split('\n')[1],
            organisation_url=None,
            site_name=SITE_NAME,
            site_url=SITE_URL
        )

        yield job
