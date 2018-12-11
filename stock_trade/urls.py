from django.conf.urls import url
from .views import trade_home, trade_update, checkout_home, checkout_done_view, share_amount
from django.urls import path, include


app_name = 'stock_info'

urlpatterns = [

    url(r'^$', trade_home, name = 'home'),
    url(r'^update/$', trade_update, name = "update"),
    url(r'^checkout/$', checkout_home, name = "checkout"),
    url(r'^checkout/success/$', checkout_done_view, name = "success"),
    url(r'^share_amount/$', share_amount, name = 'share_amount'),
    # url(r'^share$', share_amount, name = "share_amount"),
]




