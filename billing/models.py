from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


User = settings.AUTH_USER_MODEL



class BillingPortfolioManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        created = False
        obj = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user,email=user.email)
        else:
            pass

        return obj, created


# Create your models here.
class BillingPortfolio(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingPortfolioManager()

    def __str__(self):
        return self.email



def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingPortfolio.objects.get_or_create(user = instance, email= instance.email)

post_save.connect(user_created_receiver, sender= User)
