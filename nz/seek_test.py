import unittest
import requests
from .seek.spiders import seek
from nz.tests.responses import fake_response_from_file
import os

class SeekSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = seek.SeekSpider()

    def _test_job_results(self, results, expected_length):
        count = 0
        permalinks = set()
        for item in results:
            self.assertIsNotNone(item['text'])
            self.assertIsNotNone(item['title'])
            self.assertIsNotNone(item['url'])
            self.assertIsNotNone(item['organisation'])
            self.assertIsNotNone(item['city'])
            self.assertIsNotNone(item['country'])
            self.assertIsNotNone(item['sites'])
            self.assertIsNotNone(item['labels'])

        # TODO: this will delete and create objects, and should
        # only be run against a test version of Django!
        if os.environ.get('DESTRUCTIVE_TESTS', False):
            self.post_job(item)


    def _test_jobs_results(self, results, expected_length):
        count = 0
        permalinks = set()
        for item in results:
            self.assertIsNotNone(item['url'])
            self.assertIsNotNone(item['urls'])
            self.assertIsNotNone(item['next'])

    def _test_organisation_results(self, results, expected_length):
        count = 0
        permalinks = set()
        self.assertIsNotNone(results['name'])
        self.assertIsNotNone(results['url'])
        self.assertIsNotNone(results['description'])
        self.assertIsNotNone(results['city'])
        self.assertIsNotNone(results['country'])

    def test_parse(self):
        # TODO: refactor this, it was used to test the whole flow
        # in a clumsy way.

        # Get jobs
        results = self.spider.parse_jobs_page(fake_response_from_file('nz_seek/volunteering.html'))
        self._test_jobs_results(results, 10)

        # Now for each item in results we can go get the job
        # A job page, and as part of it we may have to get the associated org
        # to be able to create it -which would block job creation
        results = self.spider.parse_job_page(fake_response_from_file('nz_seek/volunteering_50715_marketing-coordinator.html'))
        self._test_job_results(results, 10)

        # This is for testing only
        results = self.spider.parse_org_page(fake_response_from_file('nz_seek/volunteering-organisations_903_west-auckland-academic-mentoring.html'))
        self._test_organisation_results(results, 10)


    def post_job(self, item):
        # TODO: in the future we do need to spin up a version of django...
        headers = {'Content-Type':'application/json',
                   'Authorization': 'Token c0fc0ee22c9902ba6b46698aa14efe4f3c7be02b'}
        payload = {'title': item['title']}
                   # Test if url or title exist

        r = requests.get('http://localhost:8000/api/jobs', params=payload, headers=headers)
        j = r.json()
        if j['count'] != 0:
            r = requests.delete('http://localhost:8000/api/jobs/{0}'.format(j['results'][0]['id']), headers=headers)
            r.raise_for_status()


        payload = {'url': item['url']}

        r = requests.get('http://localhost:8000/api/jobs', params=payload, headers=headers)
        j = r.json()
        if j['count'] != 0:
            r = requests.delete('http://localhost:8000/api/jobs/{0}'.format(j['results'][0]['id']), headers=headers)
            r.raise_for_status()

        self.assertEqual(0, j['count'])

        # Labels
        print("looking at labels")
        tmp = []
        for l in item['labels']:
            r = requests.get('http://localhost:8000/api/labels', params={'name': l}, headers=headers)
            j = r.json()
            if j['count'] > 0:
                print("found label, looking up ID")
                tmp.append(j['results'][0]['id'])
                print("found label {} id {}".format(l, j['results'][0]['id']))
            else:
                # Need to create the label
                print("creating label: {}".format(l))
                r = requests.post('http://localhost:8000/api/labels', json={'name': l}, headers=headers)
                j = r.json()
                tmp.append(j['id'])
                print("created label {} with id {}".format(l, j['id']))

        print("Labels was: %s" % item['labels'])
        item['labels'] = tmp
        print("Labels is: %s" % item['labels'])

        # Org  TODO: We should update the object if there are any changes
        #            ^^ raise issue for this
        # TODO: this fails because the name of org in the job page and
        #       org itself do not match
        r = requests.get('http://localhost:8000/api/organisations', params={'name': "{} | SEEK Volunteer".format(item['organisation'])}, headers=headers)
        j = r.json()
        print("looked for org {} and got: {}".format(item['organisation'], j))
        if j['count'] > 0:
            item['organisation_id'] = j['results'][0]['id']
        else:
            print("creating org: {}".format(item['organisation']))

            # TODO: to create an organisation, we actually need some information! Need to fix this by
            # going to referring site and finding the info, but for now, LIE
            # when doing live crawling: use r['organisation_url'] to digest the URL while we block until
            # that work has been done.
            org_object = self.spider.parse_org_page(fake_response_from_file('nz_seek/volunteering-organisations_903_west-auckland-academic-mentoring.html'))

            print("Org obj: {}".format(org_object))
            org = {'name': org_object['name'],
                   'description': org_object['description'],
                   'url': org_object['url'],
                   'region': 'placeholder', # Fuck the region for now
                   'city': org_object['city'],
                   'country': org_object['country']
                   }
            r = requests.post('http://localhost:8000/api/organisations', json=org, headers=headers)
            j = r.json()

            print("created org {} with id {}".format(item['organisation'], j['id']))
            item['organisation_id'] = (j['id'])

        print("Org name {} and id {}".format(item['organisation'], item['organisation_id']))

        # Sites
        print("looking at sites")
        tmp = []
        for i in item['sites']:
            r = requests.get('http://localhost:8000/api/sites', params={'name': i}, headers=headers)
            j = r.json()
            print("sites query returned {}".format(j))
            if j['count'] > 0:
                print("found site, looking up ID")
                tmp.append(j['results'][0]['id'])
                print("found label {} id {}".format(i, j['results'][0]['id']))
            else:
                # TODO: to create a site, we actually need some information! Need to fix this by
                # going to referring site and finding the info, but for now, LIE
                site = {'name': seek.SITE_NAME,
                       'url': seek.SITE_URL}
                print("creating site: {}".format(i))
                r = requests.post('http://localhost:8000/api/sites', json=site, headers=headers)
                print("response: {}".format(r.text))
                j = r.json()
                tmp.append(j['id'])
                print("created label {} with id {}".format(i, j['id']))

        print("Sites was: %s" % item['sites'])
        item['sites'] = tmp
        print("Sites is: %s" % item['sites'])


        r = requests.post('http://localhost:8000/api/jobs', json=item, headers=headers)
        print("item:")
        print(item)
        print("text:")
        print(r.text)
        self.assertEqual(r.status_code, 201)