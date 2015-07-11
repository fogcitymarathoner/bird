import json
from django.conf import settings

import urllib.parse
import urllib.request


def getToken(expiration, appid=None):      
    """
    Uses service to generate token from apikey and expiration
    """
    print(appid)
    print('expiration = %s'% expiration)
    if appid==None:
        url = settings.TOKENSERVER + '/issue_api_key'
        print("token server url %s"%url)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        response_data = response.read()
        print(response_data)
        data = json.loads(response_data)
        app_keytx = data['api_key']
    else:
        app_keytx = appid
    time.sleep(1)
    # params for issue token call
    url = settings.TOKENSERVER + '/issue_token'

    if isinstance(expiration, str):
        print('expiration = %s is a string'% expiration)
        expDT =datetime.datetime.strptime(expiration,'%Y-%m-%d %H:%M:%S')
    else:
        print('expiration = %s is NOT a string'% expiration)
        expDT = expiration

    #expst = expDT.strftime('%Y-%m-%d %H:%M:%S')
    print(expDT)
    data = urllib.parse.urlencode(dict(app_id=app_keytx, expiration=expDT))
    response = io.StringIO()
    crl = pycurl.Curl()
    crl.setopt(pycurl.HTTPHEADER, crlHeader)
    crl.setopt(crl.WRITEFUNCTION, response.write)
    crl.setopt(pycurl.POSTFIELDS, data)
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.SSL_VERIFYPEER, 0)
    crl.setopt(pycurl.SSL_VERIFYHOST, 0)
    crl.perform()
    data = json.loads(response.getvalue())

    appid = data['app_id']
    token = data['token']
    return appid.text, token.text

def getTokenList(appid):
    """
    Retrieves list of tokens from server for an appid
    not in api yet
    """

    values = {'app_id' : appid}
    url = settings.TOKENSERVER + '/token_list/'

    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8') # data should be bytes
    req = urllib.request.Request(url, data)
    resp = urllib.request.urlopen(req)
    respData = resp.read().decode("utf-8")

    data = json.loads(respData)
    ret = []
    for token in data:
        ret.append( [{'token':token['token'], 'expiration':token['expiration']}])
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

def tinyurl(request, token):
    view_url = request.META['wsgi.url_scheme']+'://'+request.META['HTTP_HOST']+'/tpage/'+token
    url = settings.TINYURLSERVER+'/soap/'
    print(url)
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
    print(result)
    return result
