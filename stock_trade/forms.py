from django import forms
from django.contrib.auth.models import User
from user_info.models import UserProfileInfo
from stock_trade.models import Trade


class TradeForm(forms.ModelForm):
    share_amount = forms.DecimalField()
    class Meta():
        model = Trade
        fields = ('share_amount',)



