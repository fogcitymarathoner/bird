import json
from django.conf import settings
from datetime import datetime as dt
import urllib.parse
import urllib.request

import logging
logger = logging.getLogger(__name__)

def getToken(expiration, appid=None):      
    """
    Uses service to generate token from apikey and expiration
    """
    logger.debug(appid)
    logger.debug('expiration = %s'% expiration)
    if appid==None:
        url = settings.TOKENSERVER + '/issue_api_key'
        logger.debug("token server url %s"%url)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        response_data = response.read().decode("utf-8")
        logger.debug(response_data)
        data = json.loads(response_data)
        app_keytx = data['app_id']
    else:
        app_keytx = appid

    # params for issue token call
    url = settings.TOKENSERVER + '/issue_token/' # don't forget trailing '/'

    values = {'app_id' : app_keytx,
          'expiration' : expiration,
           }
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8') # data should be bytes
    logger.debug('payload %s'%values)
    req = urllib.request.Request(url, data)
    resp = urllib.request.urlopen(req)
    respData = resp.read().decode("utf-8")

    logger.debug(respData)
    retdat = json.loads(respData)
    return retdat['app_id'], retdat['token']

def getTokenList(appid):
    """
    Retrieves list of tokens from server for an appid
    not in api yet
    """

    values = {'app_id' : appid}
    url = settings.TOKENSERVER + '/token_list/'

    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8') # data should be bytes
    logger.debug('payload %s'%values)

    req = urllib.request.Request(url, data)

    resp = urllib.request.urlopen(req)
    respData = resp.read().decode("utf-8")

    logger.debug(' token list return raw %s'%respData)
    data = json.loads(respData)
    logger.debug(' token list return %s'%data)
    ret = []
    for token in data:
        ret.append( {'token':token['token'], 'expiration':token['expiration']})
    return ret
        
def validateToken(app_id, token):

    values = {'app_id' : app_id,
          'token' : token,
           }
    url = settings.TOKENSERVER + '/validate_token/'

    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8') # data should be bytes
    req = urllib.request.Request(url, data)
    resp = urllib.request.urlopen(req)
    respData = resp.read().decode("utf-8")

    data = json.loads(respData)

    return data['value']
def validatePage(page):
    return validateToken(page.app_key, page.token)
def tinyurl(request, token):
    view_url = request.META['wsgi.url_scheme']+'://'+request.META['HTTP_HOST']+'/tpage/'+token
    url = settings.TINYURLSERVER+'/soap/'
    logger.debug(url)
    data = urllib.parse.urlencode(dict(u=view_url))
    response = io.StringIO()
    crl = pycurl.Curl()
    crl.setopt(pycurl.HTTPHEADER, crlHeader)
    crl.setopt(crl.WRITEFUNCTION, response.write)
    crl.setopt(pycurl.POSTFIELDS, data)
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.SSL_VERIFYPEER, 0)
    crl.setopt(pycurl.SSL_VERIFYHOST, 0)
    crl.perform()
    result = response.getvalue()
    logger.debug(result)
    return result
