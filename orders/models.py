from django.db import models
from stock_trade.models import Trade
from stock_market.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save

# Create your models here.


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=200, blank=True)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, default="created", choices=ORDER_STATUS_CHOICES)
    estimated_cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=5)



    def __str__(self):
        return self.order_id



    def update_estimated_cost(self):
        trade_estimated_cost = self.trade.estimated_cost
        self.estimated_cost = trade_estimated_cost
        self.save()
        return trade_estimated_cost

#generate order_id
#generate order_total




def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


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




