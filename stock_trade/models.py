from decimal import Decimal
from django.db import models
from django.conf import settings
from stock_info.models import StockInfo
# from user_info.models import UserProfileInfo
from django.db.models.signals import pre_save, post_save, m2m_changed

User = settings.AUTH_USER_MODEL


class TradeManager(models.Manager):


    def new_or_get(self, request):
        trade_id = request.session.get('trade_id', None)

        qs = self.get_queryset().filter(id=trade_id)
        if qs.count() == 1:
            new_obj = False
            # print("Trading ID exist")
            trade_obj = qs.first()
            if request.user.is_authenticated and trade_obj.user is None:
                trade_obj.user = request.user
                trade_obj.save()
        else:
            trade_obj = Trade.objects.new(user=request.user)
            new_obj = True
            request.session['trade_id'] = trade_obj.id
        return trade_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)





# Create your models here.
class Trade(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # stock_info = models.ForeignKey(StockInfo, on_delete=models.CASCADE, default=True)
    stock_info = models.ManyToManyField(StockInfo, blank=True)
    share_amount = models.DecimalField(default=1, max_digits=10, decimal_places=1)
    market_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=5)
    estimated_cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=5)

    objects = TradeManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_trade_receiver(sender, instance, action, *args, **kwargs):
    stock_info = instance.stock_info.all()

    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        # print(action)
        # print(instance.stock_info.all())
        # print(instance.estimated_cost)

        estimated_cost = 0
        for x in stock_info:
            instance.market_price = x.open
            # instance.save()
            estimated_cost += x.open
        print(estimated_cost)

        instance.estimated_cost = estimated_cost
        print(estimated_cost)

        instance.save()


m2m_changed.connect(m2m_changed_trade_receiver, sender=Trade.stock_info.through)


def pre_save_trade_receiver(sender, instance, *args, **kwargs):

    if instance.share_amount > 0:
        instance.estimated_cost = Decimal(instance.estimated_cost) * Decimal(instance.share_amount)
    else:
        instance.estimated_cost = 0.00


pre_save.connect(pre_save_trade_receiver, sender=Trade)
