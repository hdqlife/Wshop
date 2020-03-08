
from django.urls import path,include,re_path
from Buyer.views import *
urlpatterns = [
    path('index/', index),
    path('register/', register),
    path('login/', login),
    path('carts/', carts),

    path('user_center_info/', user_center_info),
    path('user_center_order/', user_center_order),
    path('user_center_site/', user_center_site),
    path('place_order/', place_order),
    re_path('detail/(?P<com_id>\d+)/', detail),
    re_path('shop_list/(?P<type_id>\d+)/(?P<page>\d+)/', shop_list),
    path('Pay/', Pay),

]