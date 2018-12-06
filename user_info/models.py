from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # DO_NOTHING)

    # portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1000),
                                                                               MaxValueValidator(99999)], default=1000)

    def __str__(self):
        return self.user.username
