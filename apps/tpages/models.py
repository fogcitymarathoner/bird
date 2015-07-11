from django.db import models
import datetime
from django.contrib.auth.models import User
class TokenizedPage(models.Model):
    app_key = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = 'bird_tokenizedpage'
    def __unicode__(self):
        return self.app_key
    
    @models.permalink
    def get_absolute_url(self):
        return ('bird.views.toolkit', [str(self.token)])

    def get_tk_url(self):
        return "/tpage/toolkit/%s" % self.token


class AccessToken(models.Model):
    token = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    expiration = models.DateTimeField(default=datetime.datetime.now)

