import scrapy
import json

from ..items import JobItem, OrganisationItem

SITE_NAME = "Do It"
SITE_URL = "https://do-it.org/"
COUNTRY = "UK"


class DoItSpider(scrapy.Spider):
    name = "do-it.org"
    allowed_domains = ["api.do-it.org"]
    start_urls = (
        # Site is heavy JS and uses API anyway
        'https://api.do-it.org/v2/opportunities',
    )

    def parse(self, response):
        """

        Example https://api.do-it.org/v2/opportunities

        Opportunities will part of a list in (under data['items']).

        Note it looks like the opportunity has the whole org object in it, we might not even have
        to get it ourselves.
            {
                "availability": {
                    "friday": [
                        true,
                        true,
                        false
                    ],
                    "monday": [
                        true,
                        true,
                        false
                    ],
                    "saturday": [
                        false,
                        false,
                        false
                    ],
                    "sunday": [
                        false,
                        false,
                        false
                    ],
                    "thursday": [
                        true,
                        true,
                        false
                    ],
                    "tuesday": [
                        true,
                        true,
                        false
                    ],
                    "wednesday": [
                        true,
                        false,
                        false
                    ]
                },
                "created": "2016-07-25T13:05:43.113705+00:00",
                "description": "They require <SNIP> activities.",
                "for_recruiter": {
                    "active_opportunities_count": 13,
                    "address_1": "Valley Springs",
                    "address_2": "",
                    "application_via_url": false,
                    "banner": [
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/banners/Activity therapy 4.1170x391.jpg",
                            "height": 391,
                            "width": 1170
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/banners/Activity therapy 4.768x391.jpg",
                            "height": 391,
                            "width": 768
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/banners/Activity therapy 4.320x391.jpg",
                            "height": 391,
                            "width": 320
                        }
                    ],
                    "blurb": "The Orchard Trust, <SNIP>
                    "charity": false,
                    "city": "Central Lydbrook",
                    "contact_name": "Tina Baker",
                    "created": "2014-10-28T14:48:46.290788+00:00",
                    "doit_approved": false,
                    "donation_page": null,
                    "email": "tina.baker@orchard-trust.org.uk",
                    "facebook": "https://www.facebook.com/pages/The-Orchard-Trust/193665117329193",
                    "id": "81ea5535-641a-48ec-aaa5-86caf68ae998",
                    "instagram": null,
                    "is_user_subscribed": false,
                    "is_volunteer_center": false,
                    "lat": 51.8395,
                    "links": [
                        {
                            "href": "/v2/orgs/the-orchard-trust",
                            "title": "The Orchard Trust Profile"
                        }
                    ],
                    "lng": -2.5796,
                    "logo": [
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/logos/Facebook_Profile.125x125.png",
                            "height": 125,
                            "width": 125
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/logos/Facebook_Profile.109x109.png",
                            "height": 109,
                            "width": 109
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/logos/Facebook_Profile.76x76.png",
                            "height": 76,
                            "width": 76
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/logos/Facebook_Profile.50x50.png",
                            "height": 50,
                            "width": 50
                        }
                    ],
                    "name": "The Orchard Trust",
                    "permissions": null,
                    "phone": "01594 861137",
                    "postcode": "GL17 9PP",
                    "rating": "0.00",
                    "rating_count": 0,
                    "slug": "the-orchard-trust",
                    "source": "doittrust",
                    "subscriber_count": 1,
                    "twitter": "https://twitter.com/OrchardTrust",
                    "website": "http://www.orchard-trust.org.uk/"
                },
                "for_recruiter_id": "81ea5535-641a-48ec-aaa5-86caf68ae998",
                "id": "3d7d6c94-882b-43a2-adb8-40b14f116b9d",
                "interests": [
                    {
                        "children": [],
                        "created": "2014-10-26T17:24:25.726228+00:00",
                        "id": "4b5f270f-723f-4aec-bbc4-6f257c3ddafa",
                        "name": "Animals",
                        "parent_id": "8e429036-c008-46cc-b1a5-ae2c739de9b9",
                        "slug": "animals",
                        "updated": "2014-10-26T17:24:25.726248+00:00"
                    },
                    {
                        "children": [],
                        "created": "2014-10-26T17:24:26.146376+00:00",
                        "id": "484cccef-29f7-463f-97e0-385657bc58da",
                        "name": "Disability",
                        "parent_id": "24620d05-41c1-4884-a0cb-f70054faba9b",
                        "slug": "disability",
                        "updated": "2014-10-26T17:24:26.146396+00:00"
                    }
                ],
                "is_new": true,
                "locations": [
                    {
                        "address_1": "Orchard Trust Smallholding",
                        "address_2": "Upper Stowfield",
                        "city": "Lower Lydbrook",
                        "county": "Gloucestershire",
                        "id": "3d7d6c94-882b-43a2-adb8-40b14f116b9d",
                        "lat": 51.8395,
                        "lng": -2.57958,
                        "local_authority": {
                            "id": "1c77b7ea-327f-492e-af78-5fe686308283",
                            "name": "Forest of Dean District",
                            "slug": "forest-of-dean-district"
                        },
                        "location": null,
                        "location_id": null,
                        "location_name": null,
                        "location_type": "SL",
                        "places_available": 1,
                        "postcode": "GL17 9PP",
                        "rating": "0.00",
                        "rating_count": 0,
                        "working_from_home": false
                    }
                ],
                "micro_availability": [],
                "owner_recruiter": {
                    "active_opportunities_count": 297,
                    "address_1": "CCP - Cheltenham Volunteer Centre",
                    "address_2": "340 High Street",
                    "application_via_url": false,
                    "banner": [
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com
                            /media.do-it.org/orgs/banners/use for VG header.1170x391.jpg",
                            "height": 391,
                            "width": 1170
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/banners/use for VG header.768x391.jpg",
                            "height": 391,
                            "width": 768
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/banners/use for VG header.320x391.jpg",
                            "height": 391,
                            "width": 320
                        }
                    ],
                    "blurb": "Volunteering Gloucestershire <SNIP>
                    "charity": false,
                    "city": "Cheltenham",
                    "contact_name": "Steve Harris",
                    "created": "2014-10-28T14:46:59.495566+00:00",
                    "doit_approved": true,
                    "donation_page": null,
                    "email": "info@volunteerglos.org.uk",
                    "facebook": "https://www.facebook.com/volunteerglos",
                    "id": "076ff95c-9262-4af7-976b-e96e85d38cd7",
                    "instagram": null,
                    "is_user_subscribed": false,
                    "is_volunteer_center": true,
                    "lat": 51.900101,
                    "links": [
                        {
                            "href": "/v2/orgs/volunteering-gloucestershire",
                            "title": "Volunteering Gloucestershire Profile"
                        }
                    ],
                    "lng": -2.0791,
                    "logo": [
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/

                            media.do-it.org/orgs/logos/VG-BV&CTsq.125x125.jpg",
                            "height": 125,
                            "width": 125
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/logos/VG-BV&CTsq.109x109.jpg",
                            "height": 109,
                            "width": 109
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com
                            /media.do-it.org/orgs/logos/VG-BV&CTsq.76x76.jpg",
                            "height": 76,
                            "width": 76
                        },
                        {
                            "absolute_url": "https://s3-eu-west-1.amazonaws.com/
                            media.do-it.org/orgs/logos/VG-BV&CTsq.50x50.jpg",
                            "height": 50,
                            "width": 50
                        }
                    ],
                    "name": "Volunteering Gloucestershire",
                    "permissions": null,
                    "phone": "0300 365 6700",
                    "postcode": "GL50 3JF",
                    "rating": "0.00",
                    "rating_count": 0,
                    "slug": "volunteering-gloucestershire",
                    "source": "doittrust",
                    "subscriber_count": 62,
                    "twitter": "http://twitter.com/volunteerglos",
                    "website": "http://www.volunteerglos.org.uk"
                },
                "owner_recruiter_id": "076ff95c-9262-4af7-976b-e96e85d38cd7",
                "photo": [],
                "specific_end_date": null,
                "specific_start_date": "2017-10-25T08:47:07.799000+00:00",
                "status": "live",
                "title": "Smallholding Support (working with animals)",
                "updated": "2017-10-25T08:48:30.722209+00:00"
            },


        Next links will be here (under data):

        "links": {
            "next": {
                "href": "/v2/opportunities?page=2",
                "title": "Next page"
            },
        "self": {
            "href": "/v2/opportunities",
            "title": "You are here."
        }
    },

        :param response:
        :return: Scrapy Request generators
        """

        jsonresponse = json.loads(response.body_as_unicode())

        for job in jsonresponse['data']['items']:
            yield self.parse_job_page(job)  # Is this the right way to do it?

        next_page_url = jsonresponse['links']['next']
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_job_page(self, job):
        """
        Parse a job and yield it for a pipeline to create.
        :param job:
        :return a SeekJobItem generator:
        """

        # TODO: transform / translate JSON into job object
        job = JobItem(
            # title=response.xpath('/html/head/meta[contains(@property, "og:title")]/@content').extract_first(),
            # url=response.xpath('/html/head/meta[contains(@property, "og:url")]/@content').extract_first(),
            # text="\n".join(response.xpath('//div[@id="opp-desc"]/p/text()').extract()),
            # labels=m[0].split(","),
            # city=m[2],
            # sites=[SITE_NAME],
            # region="placeholder",
            # country=COUNTRY,
            # organisation=response.xpath('//p[@class="byline"]/strong/a/text()').extract_first(),
            # organisation_url=response.xpath('//p[@class="byline"]/strong/a/@href').extract_first(),
            # site_name=SITE_NAME,
            # site_url=SITE_URL,
        )

        yield job

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
        org = OrganisationItem(
            # name=response.xpath('/html/head/meta[contains(@property, "og:title")]/@content').extract_first(),
            # url=response.xpath('/html/head/meta[contains(@property, "og:url")]/@content').extract_first(),
            # description=response.xpath('//div[@id="org-desc"]/p/text()').extract_first(),
            # city=response.xpath('//div[@class="snapshot"]/p/span/text()').extract_first(),
            # region="placeholder",
            # # TODO: add tags too!?
            # country=COUNTRY,
        )

        return org
