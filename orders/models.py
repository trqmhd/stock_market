from django.db import models
from stock_trade.models import Trade
from stock_market.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
from math import fsum
from billing.models import BillingPortfolio
# Create your models here.


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_portfolio, trade_obj):
        created = False
        qs = Order.objects.filter(billing_portfolio=billing_portfolio, trade=trade_obj, active=True, status = 'created')
        if qs.count() == 1:

            obj = qs.first()
        else:
            # old_order_qs = Order.objects.exclude(billing_portfolio = billing_portfolio).filter(trade = trade_obj, active = True)
            # if old_order_qs.exists():
            #     old_order_qs.update(active = False)
            obj = Order.objects.create(billing_portfolio=billing_portfolio, trade=trade_obj)
            created = True
        return obj, created





class Order(models.Model):
    billing_portfolio = models.ForeignKey(BillingPortfolio,null=True, blank=True,  on_delete=models.CASCADE)
    order_id = models.CharField(max_length=200, blank=True)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, default="created", choices=ORDER_STATUS_CHOICES)
    estimated_cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=5)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    def update_estimated_cost(self):
        trade_estimated_cost = self.trade.estimated_cost
        print(type(trade_estimated_cost))

        self.estimated_cost = format(trade_estimated_cost, '.2f')
        self.save()
        return trade_estimated_cost

#generate order_id
#generate order_total

    def check_done(self):
        billing_portfolio = self.billing_portfolio
        estimated_cost = self.estimated_cost
        # if self.estimated_cost < 0:
        #     return False
        if billing_portfolio and estimated_cost > 0:
            return True
        return False


    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status




def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(trade = instance.trade).exclude(billing_portfolio = instance.billing_portfolio)
    if qs.exists():
        qs.update(active = False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_trade_estimated_cost(sender, instance,created,  *args, **kwargs):
    if not created:
        trade_obj = instance
        trade_estimated_cost = trade_obj.estimated_cost
        trade_id = trade_obj.id
        qs = Order.objects.filter(trade__id=trade_id)

        if qs.exists() == 1:
            order_obj = qs.first()
            order_obj.update_estimated_cost()


post_save.connect(post_save_trade_estimated_cost, sender=Trade)



def post_save_order(sender, instance, created, *args, **kwargs):
    print("Running.....")
    if created:
        print("Updating .....")
        instance.update_estimated_cost()

post_save.connect(post_save_order, sender=Order)




