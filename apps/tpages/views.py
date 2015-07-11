from django.shortcuts import  get_object_or_404, render_to_response

from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from tpages.models import TokenizedPage
from tpages.models import AccessToken
from tpages.forms import PageAddForm, PageEditForm

from django.template import RequestContext

from tpages.lib import getToken, getTokenList, validateToken, tinyurl
from datetime import datetime as dt
import time
from datetime import datetime, date, timedelta
from pprint import pprint

uri = '' #settings.APP_URI
@login_required
def ninetymoredays(request,token):
    print('in view page')
    page = get_object_or_404(TokenizedPage,
                             token=token
    )
    print(('got page %s'%page))
    ninety = datetime.now() + timedelta(days=90)
    exp = ninety.strftime("%m/%d/%Y")
    print(exp)
    expDT =datetime.strptime(exp,'%m/%d/%Y')
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
    return HttpResponseRedirect('/tpage/'+token) # Redirect after POST

@login_required
def add(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PageAddForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data           
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            exp = form.cleaned_data['expiration_date']
            print(('expiration %s'%exp))
            #expdate = time.strptime(exp.str,'%Y-%m-%d')
        #print datetime.strptime('31/07/2013', "%d/%m/%Y").strftime("%Y-%m-%d")
            if body is not None:

                appid, token = getToken(exp)
                page = TokenizedPage(app_key=appid, token=token, body=body, title=title)
                page.save()
                return HttpResponseRedirect(uri+'tpage/toolkit/'+token) # Redirect after POST
                pass
            else:
                pass
    else:
        form = PageAddForm() # An unbound form
    return render_to_response('tpages/tokenized_page_add.html',
                              {
                               'form': form,
                               },
                context_instance=RequestContext(request)
                              )

@login_required
def edit(request, token):
    if request.method == 'POST': # If the form has been submitted...
        
        pprint(request.POST)
        form = PageAddForm(request.POST) # A form bound to the POST data
        pprint(request.POST)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data           
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            app_key = request.POST['app_key']
            print(app_key)
            if body is not None:
                
                page = get_object_or_404(TokenizedPage,
                                    app_key=app_key
                                    )
                page.body = body
                page.title = title
                page.save()
                tokens = getTokenList(page.app_key);
                for tokentmp in tokens:
                    if tokentmp[0]['token'] == token:
                        page.expiration = tokentmp[0]['expiration']

                return HttpResponseRedirect(uri+'tpage/toolkit/'+token) # Redirect after POST
                pass
            else:
                pass
    else:
        
        page = get_object_or_404(TokenizedPage,token=token)
        form = PageEditForm(instance=page) 

        tokens = getTokenList(page.app_key);
        exp = dt.now()
        for tokentmp in tokens:
            if tokentmp[0]['token'] == token:
                page.expiration = tokentmp[0]['expiration']
                struct_time = time.strptime(page.expiration, "%Y-%m-%d %H:%M:%S %Z")

                exp = datetime.fromtimestamp(time.mktime(struct_time))

        return render_to_response('tpages/tokenized_page_edit.html',
                              {
                               'page': page,
                               'form': form,
                               'expiration': exp.strftime("Page access expires %m/%d/%Y."),
                               },
                context_instance=RequestContext(request)
                              )

@login_required
def delete(request,token):
    page = get_object_or_404(TokenizedPage,
                                    token=token
                                    )
    page.delete()
    return HttpResponseRedirect(uri+'tpage/') # Redirect after POST

@login_required
def toolkit(request, token):

    page = get_object_or_404(TokenizedPage, token=token)
    page.status = validateToken(page.app_key, token)



    return render_to_response('tpages/tokenized_page_toolkit.html',
                          {
                           'page': page,
                           'tinyurl': 'tiny url is broken',
                           },
            context_instance=RequestContext(request)
                          )
def show(request, token):
    if request.method == 'POST': # If the form has been submitted...
        #form = PageEditForm(request.POST) # A form bound to the POST data
        #if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect(uri+'thanks/') # Redirect after POST
    else:
        page = get_object_or_404(TokenizedPage,
                                    token=token
                                    )

        if validateToken(page.app_key,token) :
            print('###############################################')
            print('###############################################')
            print('token did validate')
            print('###############################################')
            print('###############################################')
            tokens = getTokenList(page.app_key);
            print('tokens')
            print(tokens)
            for tokentmp in tokens:
                if tokentmp[0]['token'] == token:
                    page.expiration = tokentmp[0]['expiration']
                    print((page.expiration))
                    
                    
                    struct_time = time.strptime(page.expiration, "%Y-%m-%d %H:%M:%S %Z")
                    pprint (struct_time)
                    dt = datetime.fromtimestamp(time.mktime(struct_time))
            return render_to_response('tpages/tokenized_page_showpage.html',
                              {
                               'page': page,
                               'expiration': dt.strftime("Page access expires %m/%d/%Y."),
                               'tinyurl': 'tinyurl is broke',#tinyurl(request, token),
                               },
                context_instance=RequestContext(request)
                              )       
        else:
            print('###############################################')
            print('###############################################')
            print('token did not validate')
            print('###############################################')
            print('###############################################')

            return HttpResponseRedirect(uri+'thanks/') # Redirect after POST
        
@login_required
def list(request):
    return render_to_response('tpages/tokenized_page_index.html',
                              {
                               'object_list':TokenizedPage.objects.all()
                               },
                context_instance=RequestContext(request)
                              )

