from django.conf.urls import url
from user_info import views
from django.urls import path, include

app_name = 'user_info'

urlpatterns = [

    url(r'^register/$', views.register, name='register'),
    # path('user_info/', include('user_info.url'))
    url(r'^user_login/$', views.user_login, name='user_login')

]
