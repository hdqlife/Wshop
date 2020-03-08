from django.shortcuts import render,HttpResponse
from Store.models import *
from django.core.paginator import *
from Wshop.views import *
from Buyer.models import *

@loginValid_buyer
def index(request):
    types = Type.objects.filter(parent=0)
    result = []
    for t in types:
        d = {}
        d["type"] = t
        d["data"] = t.commodity_set.filter(delete_flage="false").order_by("commodity_data")[:4]
        result.append(d)
    return render(request,"Buyer/index.html",locals())
# Create your views here.


@loginValid_buyer
def shop_list(request,type_id,page):
    page_int = int(page)
    commoditys = Type.objects.get(id = int(type_id)).commodity_set.filter(delete_flage="false")
    paginator = Paginator(commoditys,10)
    page = paginator.page(page_int)
    if page_int < 4:
        page_range = range(1,6)
    else:
        page_range = paginator.page_range[page_int-3:page_int+2]
    if page == 1:
        previous_page = 0
    else:
        previous_page = page_int-1
    next_page = page_int+1
    return render(request,"buyer/list.html",{"commoditys":page,  #页面数据
                                             "type_id":type_id,    #页码范围
                                             "page_range":page_range,   #类型
                                             "previous_page":previous_page,   #上一页
                                             "next_page":next_page})    #下一页

@loginValid_buyer
def detail(request,com_id):
    commodity = Commodity.objects.get(id = int(com_id))
    if request.method == "POST":
        number = request.POST.get("number")
        car = BuyCar()
        car.commodity_name = commodity.commodity_name
        car.commodity_id = commodity.id
        car.commodity_price = commodity.commodity_price
        car.commodity_picture = commodity.commodity_picture
        car.commodity_number = number

        car.shop_id = commodity.shop_id
        car.user_id = request.COOKIES.get("user_id")
        car.save()
        return HttpResponseRedirect("/Buyer/carts/")
    return render(request,"buyer/detail.html",locals())

def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")

        user = BuyUser()
        user.login_name = username
        user.password = setPassword(password)
        user.save()
        return HttpResponseRedirect("/Buyer/login/")
    return render(request,"buyer/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        user = BuyUser.objects.filter(login_name=username).first()
        if user:
            db_password = user.password
            form_password = setPassword(password)
            if db_password == form_password:
                response = HttpResponseRedirect("/")
                response.set_cookie("username",user.login_name)
                response.set_cookie("user_id",user.id)
                return response

    return render(request,"buyer/login.html")

@loginValid_buyer
def carts(request):
    user_id = int(request.COOKIES.get("user_id"))
    shop_list = BuyCar.objects.filter(user_id = user_id)
    shops = []
    for shop in shop_list:
        shops.append({
            "id":shop.id,
            "commodity_name":shop.commodity_name,
            "commodity_id":shop.id,
            "commodity_price":shop.commodity_price,
            "commodity_number":shop.commodity_number,
            "commodity_picture":shop.commodity_picture,
            "total":shop.commodity_price * shop.commodity_number,
        })
    shops = shops[::-1]
    return  render(request,"buyer/carts.html",locals())




@loginValid_buyer
def place_order(request):
    if request.method == "POST":
        add_list = Address.objects.all()
        data = request.POST
        car_shop_list = []
        for k,v in data.items():
            if v == "on":
                car_data = BuyCar.objects.get(id = int(k))
                car_shop_list.append(car_data)
        car_shop_list = enumerate(car_shop_list,1)
        return  render(request,"buyer/place_order.html",locals())
    else:
        return HttpResponse("bad request method")
@loginValid_buyer
def user_center_info(request):
    return render(request,"buyer/user_center_info.html")
@loginValid_buyer
def user_center_order(request):
    return render(request,"buyer/user_center_order.html")
@loginValid_buyer
def user_center_site(request):
    add_list = Address.objects.all()

    if request.method == "POST":
        recver = request.POST.get("recver")
        addr = request.POST.get("address")
        phone = request.POST.get("phone")

        address = Address()
        address.address = addr
        address.recver = recver
        address.phone = phone
        address.buyer_id = BuyUser.objects.get(id = int(request.COOKIES.get("user_id")))
        address.save()
    return render(request,"buyer/user_center_site.html",locals())

import datetime
from Wshop.views import pay
def Pay(request):
    if request.method == "GET" and request.GET:
        data = request.GET
        data_itme = data.items()
        order = Order()
        order.user_address = Address.objects.get(id=1)
        order.state = 0
        order.date = datetime.datetime.now()
        order.user_id = BuyUser.objects.get(id = int(request.COOKIES.get("user_id")))
        order.save()
        order.order_number = "sp"+str(order.id).zfill(7)
        order.save()
        money = 0

        for k,v in data_itme:
            if k.startswith("shop_"):
                car_id = int(v)
                data = BuyCar.objects.get(id = car_id)
                order_reource = OrderResource()
                order_reource.commodity_name=data.commodity_name
                order_reource.commodity_id=data.commodity_id
                order_reource.commodity_price=data.commodity_price
                order_reource.commodity_number=data.commodity_number
                order_reource.commodity_picture=data.commodity_picture
                order_reource.small_money=data.commodity_price*data.commodity_number
                order_reource.order_id=order
                order_reource.store_id=Store.objects.get(id=data.shop_id)
                order_reource.save()
                money += order_reource.small_money
        order.money = money
        url = pay(order.order_number,order.money)
        return HttpResponseRedirect(url)
