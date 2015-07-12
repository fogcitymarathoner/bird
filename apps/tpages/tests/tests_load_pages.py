__author__ = 'marc'
from datetime import datetime as dt
from django_webtest import WebTest

from django.core.urlresolvers import reverse
from tpages.models import TokenizedPage

class SimpleLoadPagesTest(WebTest):
    def setUp(self):
        token = 'abc'
        appid = 'xyz'
        body = 'hi body'
        title = 'hi title'
        page = TokenizedPage(app_key=appid, token=token, body=body, title=title)
        page.save()
    def tearDown(self):
        pass

    def test_load_pages(self):

        url = reverse('tpages:edit', args=(), kwargs={'token': 'abc'})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)


        url = reverse('tpages:delete', args=(), kwargs={'token': 'abc'})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)


        url = reverse('tpages:toolkit', args=(), kwargs={'token': 'abc'})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)



        url = reverse('tpages:ninetymoredays', args=(), kwargs={'token': 'abc'})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)


        url = reverse('tpages:show', args=(), kwargs={'token': 'abc'})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)


        url = reverse('tpages:list', args=(), kwargs={})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)



        url = reverse('tpages:add', args=(), kwargs={})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)