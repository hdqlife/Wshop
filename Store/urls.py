
from django.urls import path,include,re_path
from Store.views import *
urlpatterns = [
    path('login/', login),
    path('index/', index),
    path('register/', register),
    path('logout/', logout),
    path('addType/', addType),
    re_path('listType/(?P<type>\w+)/(?P<page>\d+)/(?P<value>\d+)/', listType),
    path('addCommodity/', addCommodity),
    re_path('listCommodity/(?P<type>\w+)/(?P<page>\d+)/', listCommodity),
    re_path('soldCommodity/(?P<type>\w+)/(?P<id>\d+)/', soldCommodity),
    path('order_list/', order_list)
]

urlpatterns += [
    path('addData/', addData),
]