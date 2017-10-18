import scrapy

# TODO: import vol model
# TODO: import these too
SITE_NAME = "SEEK Volunteer"
SITE_URL = "https://seekvolunteer.co.nz/"
COUNTRY = "NZ"

class SeekSpider(scrapy.Spider):
    name = "dummy"
    allowed_domains = ["example.com", "iana.org"]
    start_urls = (
        'http://www.example.com/',
    )

    def parse_jobs_page(self, response):
        # TODO: we should yield, and use models
        r = {}
        r['url'] = response.xpath('/html/head/meta[contains(@property, "og:url")]/@content').extract_first()
        r['urls'] = response.css("#search-result").css("li").css("div.col-md-9 header h2 a::attr(href)").extract()
        r['next'] = response.css("#search-result").css("nav span.next a::attr(href)").extract()[0]

        print(r)
        return [r]

    def parse_job_page(self, response):
        # TODO: don't return, yield, and use item (or model)
        r = {}
        r['title'] = response.xpath('/html/head/meta[contains(@property, "og:title")]/@content').extract_first()
        r['url'] = response.xpath('/html/head/meta[contains(@property, "og:url")]/@content').extract_first()
        r['text'] = "".join(response.xpath('//div[@id="opp-desc"]/p/text()').extract())

        # Boy this is pure poetry ;(
        m = response.xpath('//div[@class="infobar snapshot"]/span/text()').extract()
        r['labels'] = m[0].split(",")
        r['city'] = m[2]
        # r['region'] = "foo" # What should this be? Ignore completely? How does it map internationally?
        r['sites'] = [SITE_NAME]
        r['country'] = COUNTRY

        r['organisation'] = response.xpath('//p[@class="byline"]/strong/a/text()').extract_first()
        r['organisation_url'] = response.xpath('//p[@class="byline"]/strong/a/@href').extract_first()

        print(r)
        return [r]

    def parse_org_page(self, response):
        # TODO: we should yield, and use models
        r = {}
        r['name'] = response.xpath('/html/head/meta[contains(@property, "og:title")]/@content').extract_first()
        r['url'] = response.xpath('/html/head/meta[contains(@property, "og:url")]/@content').extract_first()

        r['description'] = response.xpath('//div[@id="org-desc"]/p/text()').extract_first()
        r['city'] =response.xpath('//div[@class="snapshot"]/p/span/text()').extract_first()

        # TODO: add tags too!?

        r['country'] = COUNTRY
        print(r)
        return r