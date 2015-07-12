from django.core.management.base import BaseCommand, CommandError
from datetime import datetime as dt
from datetime import timedelta as td
from tpages.models import TokenizedPage

from tpages.lib import getToken, getTokenList, validateToken, tinyurl
class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        add 90 more days to tokens expiration on pages
        :param args:
        :param options:
        :return:
        """
        pages = TokenizedPage.objects.all()
        for page in pages:

            print(('got page %s'%page))
            ninety = dt.now() + td(days=90)
            exp = ninety.strftime("%m/%d/%Y")
            print(exp)
            expDT = dt.strptime(exp,'%m/%d/%Y')
            expst = expDT.strftime('%Y-%m-%d %H:%M:%S')
            print(expst)

            appid, token = getToken(expst)
            page.app_key = appid
            page.token = token
            print('##########################################')
            print('##########################################')
            print('##########################################')
            print('new token')
            print(('apiid = %s'%appid))
            print(('token =%s'%token))
            print('##########################################')
            print('##########################################')
            page.save()