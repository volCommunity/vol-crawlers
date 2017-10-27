import scrapy

from ..items import JobItem, OrganisationItem

SITE_NAME = "SEEK Volunteer"
SITE_URL = "https://seekvolunteer.co.nz/"
COUNTRY = "NZ"


class SeekSpider(scrapy.Spider):
    name = "seekvolunteer.co.nz"
    allowed_domains = ["seekvolunteer.co.nz"]
    start_urls = (
        # 'https://seekvolunteer.co.nz/volunteering?interest_ids%5b%5d=30',
        'https://seekvolunteer.co.nz/volunteering',
    )

    def parse(self, response):
        """
        :param response:
        :return: Scrapy Request generators
        """
        job_urls = response.css("#search-result").css("li").css("div.col-md-9 header h2 a::attr(href)").extract()
        for job_url in job_urls:
            yield scrapy.Request(response.urljoin(job_url), callback=self.parse_job_page)

        next_page_url = response.css("#search-result").css("nav span.next a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_job_page(self, response):
        """
        Parse a job and yield it for a pipeline to create.
        :param response:
        :return a SeekJobItem generator:
        """
        m = response.xpath('//div[@class="infobar snapshot"]/span/text()').extract()

        job = JobItem(
            title=response.xpath('/html/head/meta[contains(@property, "og:title")]/@content').extract_first(),
            url=response.url,
            text="\n".join(response.xpath('//div[@id="opp-desc"]/p/text()').extract()),
            labels=m[0].split(","),
            city=m[2],
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
        org = OrganisationItem(
            name=response.xpath('/html/head/meta[contains(@property, "og:title")]/@content').extract_first(),
            url=response.url,
            description=response.xpath('//div[@id="org-desc"]/p/text()').extract_first(),
            city=response.xpath('//div[@class="snapshot"]/p/span/text()').extract_first(),
            region="placeholder",
            # TODO: add tags too!?
            country=COUNTRY,
        )

        return org
