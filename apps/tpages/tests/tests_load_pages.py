__author__ = 'marc'
from datetime import datetime as dt
from datetime import timedelta as td
from django_webtest import WebTest

from django.core.urlresolvers import reverse
from tpages.models import TokenizedPage

from tpages.lib import getToken
import pytz

utc=pytz.UTC
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

        # 404 not testable
        #url = reverse('tpages:show', args=(), kwargs={'token': 'abc'})
        #response = self.app.get(url)
        #self.assertEqual(response.status_code, 404)


        url = reverse('tpages:list', args=(), kwargs={})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)



        url = reverse('tpages:add', args=(), kwargs={})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)




class SimpleLoadBadPagesTest(WebTest):
    def setUp(self):
        body = 'hi body'
        title = 'hi title'
        expiration = dt.now() + td(days=1)
        self.appid, self.token = getToken(utc.localize(expiration).strftime("%Y-%m-%d %H:%M:%S"))
        page = TokenizedPage(app_key=self.appid, token=self.token, body=body, title=title)
        page.save()
    def tearDown(self):
        pass

    def test_load_pages(self):
        # 404 not testable
        #url = reverse('tpages:show', args=(), kwargs={'token': self.token})
        #response = self.app.get(url)
        #self.assertEqual(response.status_code, 302)
        pass