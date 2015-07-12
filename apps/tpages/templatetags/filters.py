from django import template
from datetime import datetime as dt
from tpages.lib import getTokenList, validatePage
import time

register = template.Library()


@register.filter(name='expiration')
def expiration(value):
    """
    return string containing page expiration
    :param value:
    :return:
    """

    tokens = getTokenList(value.app_key);
    print('tokens')
    exp = dt.now()
    for tokentmp in tokens:
        if tokentmp['token'] == value.token:
            value.expiration = tokentmp['expiration']
            print((value.expiration))


            struct_time = time.strptime(value.expiration, "%Y-%m-%d %H:%M:%S")
            print (struct_time)
            exp = dt.fromtimestamp(time.mktime(struct_time))
    return exp.strftime("Page access expires %m/%d/%Y.")

@register.filter(name='page_valid')
def page_valid(page):

    status = validatePage(page)
    return 'page valid %s'%status

@register.filter(name='pub_date')
def pub_date(page):

    return page.pub_date.strftime("%Y-%m-%d")