from django.core.management.base import BaseCommand, CommandError
from datetime import datetime as dt
from datetime import timedelta as td
from tpages.models import TokenizedPage

from tpages.lib import getToken, getTokenList, validateToken, tinyurl

import logging
logger = logging.getLogger(__name__)
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

            logger.debug(('got page %s'%page))
            ninety = dt.now() + td(days=90)
            exp = ninety.strftime("%m/%d/%Y")
            logger.debug(exp)
            expDT = dt.strptime(exp,'%m/%d/%Y')
            expst = expDT.strftime('%Y-%m-%d %H:%M:%S')
            logger.debug(expst)

            appid, token = getToken(expst)
            page.app_key = appid
            page.token = token
            logger.debug('##########################################')
            logger.debug('##########################################')
            logger.debug('##########################################')
            logger.debug('new token')
            logger.debug(('apiid = %s'%appid))
            logger.debug(('token =%s'%token))
            logger.debug('##########################################')
            logger.debug('##########################################')
            page.save()