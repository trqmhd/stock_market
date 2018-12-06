from django.db import models
import django.db.models.fields
from user_info.models import UserProfileInfo
from django.conf.urls import url, include
# from .views import StockDetailView
from stock_market.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save




class StockManager(models.Manager):
    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

# Create your models here.








class StockInfo(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    slug = models.SlugField(blank=True, unique=True)
    high = models.DecimalField(max_digits=15, decimal_places=7, null=True)
    low = models.DecimalField(max_digits=15, decimal_places=7, null=True)
    open = models.DecimalField(max_digits=15, decimal_places=7, null=True)
    close = models.DecimalField(max_digits=15, decimal_places=7, null=True)
    volume = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    adj_close = models.DecimalField(max_digits=15, decimal_places=7, null=True)

    # user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    # timestamp = models.DateTimeField(auto_now_add=True)

    objects = StockManager()

    def get_absolute_url(self):
        #return ("{}".format(self.id))
        return ("/stock/{slug}/".format(slug =self.slug))

    def __str__(self):
        return self.symbol

    @property
    def name(self):
        return self.symbol


def stock_info_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)  #"abc"

pre_save.connect(stock_info_pre_save_receiver, sender=StockInfo)
