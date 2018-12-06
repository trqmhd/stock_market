"""stock_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user_info import views
from django.conf.urls import url, include
from stock_info.views import StockListView, stock_list_view, StockDetailView, stock_detail_view, SearchStockView, StockDetailSlugView
from stock_trade.views import trade_home



urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', views.index, name='index'),

    url(r'^user_info/', include('user_info.urls')),

    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'special/', views.special, name='special'),

    url(r'^stock/$', StockListView.as_view(), name='StockListView'),
    url(r'^stock-fbv/$', stock_list_view),

   # url(r'^stock/(?P<pk>\d+)/$', StockDetailView.as_view()),
    url(r'^stock-fbv/(?P<pk>\d+)/$', stock_detail_view),

    url(r'^search/$', SearchStockView.as_view(), name="search"),
    # url(r'^search/$', SearchStockView, name = 'search'), #search stock - function search

    url(r'^search/(?P<pk>\d+)$', StockDetailView.as_view()),  # search and the detailing of the stock


    #url(r'^trade/$', trade_home, name='trade'),
    url(r'^trade/', include("stock_trade.urls", namespace='trade')),


    url(r'^stock/(?P<slug>[\w-]+)/$', StockDetailSlugView.as_view()),

]
