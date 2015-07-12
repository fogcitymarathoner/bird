__author__ = 'marc'

import re

from django.test import TestCase

from django.core.urlresolvers import reverse

class SimpleReverseUrlsTest(TestCase):

    def test_reverse_urls(self):
        """
        Clients - test the reverse urls for the exposed display pages
        """

        url = reverse('tpages:edit', args=(), kwargs={'token': 'clients'})
        print(url)
        pattern = '^/tpages/edit/clients'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('tpages:delete', args=(), kwargs={'token': 'clients'})
        print(url)
        pattern = '^/tpages/delete/clients'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('tpages:toolkit', args=(), kwargs={'token': 'clients'})
        print(url)
        pattern = '^/tpages/toolkit/clients'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('tpages:ninetymoredays', args=(), kwargs={'token': 'clients'})
        print(url)
        pattern = '^/tpages/ninetymoredays/clients'
        matched = re.search(pattern, url)
        self.assertTrue(matched)



        url = reverse('tpages:show', args=(), kwargs={'token': 'clients'})
        print(url)
        pattern = '^/tpages/clients'
        matched = re.search(pattern, url)
        self.assertTrue(matched)



        url = reverse('tpages:list', args=(), kwargs={})
        print(url)
        pattern = '^/tpages/'
        matched = re.search(pattern, url)
        self.assertTrue(matched)



        url = reverse('tpages:add', args=(), kwargs={})
        print(url)
        pattern = '^/tpages/add'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

