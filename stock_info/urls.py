from django.conf.urls import url
from stock_info import views
from django.urls import path, include


app_name = 'stock_info'

urlpatterns = [
    #url(r'^$', views.stock_index, name = 'stock_index'),
    #url(r'^stock_info/', include('stock_info.urls')),
]

