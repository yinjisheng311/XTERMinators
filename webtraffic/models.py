from django.db import models
# from django.utils import timezone
# import datetime

# Create your models here.
class ReceivedData(models.Model):
    host_name = models.CharField(max_length=20) #eg h1, h2
    packet_size_byte = models.IntegerField()
    is_retransmitted = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class SentData(models.Model):
    host_name = models.CharField(max_length=20) #eg h1, h2
    packet_size_byte = models.IntegerField()
    is_retransmitted = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'