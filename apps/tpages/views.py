from django.shortcuts import  get_object_or_404, render_to_response

from django.http import HttpResponseRedirect
from django.http import Http404
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from tpages.models import TokenizedPage

from tpages.forms import PageForm
from tpages.models import TokenizedPage

from django.template import RequestContext

from tpages.lib import getToken, getTokenList, validateToken, tinyurl
from datetime import datetime as dt
import time
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse


@login_required
def ninetymoredays(request, token):
    print('in view page')
    page = get_object_or_404(TokenizedPage,token=token)
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
    return HttpResponseRedirect(reverse('tpages:toolkit', args=(), kwargs={'token': token})) # Redirect after POST

@login_required
def add(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PageForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            appid, token = getToken(form.cleaned_data['expiration'].strftime("%Y-%m-%d %H:%M:%S"))
            page = TokenizedPage(app_key=appid, token=token, body=body, title=title)
            page.save()
            return HttpResponseRedirect(reverse('tpages:toolkit', args=(), kwargs={'token': token})) # Redirect after POST

    else:
        form = PageForm() # An unbound form
    return render_to_response('tpages/tokenized_page_add.html',{'form': form,},context_instance=RequestContext(request))

@login_required
def edit(request, token):
    if request.method == 'POST': # If the form has been submitted...
        
        print(request.POST)
        form = PageForm(request.POST) # A form bound to the POST data
        print(request.POST)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data           

            page = get_object_or_404(TokenizedPage, app_key=token)
            page.body = form.cleaned_data['body']
            page.title = form.cleaned_data['title']
            page.save()

            return HttpResponseRedirect(reverse('tpages:toolkit', args=(), kwargs={'token': page.app_key})) # Redirect after POST

    else:
        
        page = get_object_or_404(TokenizedPage,token=token)
        form = PageForm(instance=page)

        tokens = getTokenList(page.app_key);
        # in case there are no tokens?
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
    """
    delete the tokenized pages after verifying
    :param request:
    :param token:
    :return:
    """
    page = get_object_or_404(TokenizedPage, token=token)
    page.delete()
    return HttpResponseRedirect(reverse('tpages:list', args=(), kwargs={})) # Redirect after POST

@login_required
def toolkit(request, token):

    page = get_object_or_404(TokenizedPage, token=token)
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
            return Http404('bad page')
    else:
        page = get_object_or_404(TokenizedPage,token=token)

        if validateToken(page.app_key,token) :
            print('###############################################')
            print('###############################################')
            print('token %s did validate'%token)
            print('with %s appkey'%page.app_key)
            print('###############################################')
            print('###############################################')
            return render_to_response('tpages/tokenized_page_showpage.html',
                              {
                               'page': page,
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

            return Http404('bad page') # Redirect after POST
        
@login_required
def list(request):
    return render_to_response('tpages/tokenized_page_index.html',
                              {'object_list':TokenizedPage.objects.all()},
                                context_instance=RequestContext(request))

