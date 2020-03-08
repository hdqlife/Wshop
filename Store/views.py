from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from Store.models import *
from Wshop.views import *
from django.core.paginator import *
import random

@loginValid
def index(request):
    return render(request,'Store/index.html')
# Create your views here.

def login(request):
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")

        store = Store.objects.filter(login_name=username).first()
        if store:
            form_password = setPassword(password)
            db_password = store.password

            if form_password == db_password:
                response = HttpResponseRedirect("/Store/index/")
                response.set_cookie("username",store.login_name)
                return response

    return render(request,'Store/login.html')

def register(request):
    if request.method == "POST" and request.POST:
        data = request.POST
        img = request.FILES.get("logo")
        store = Store()
        store.store_name = data.get("store_name")
        store.login_name = data.get("username")
        store.password = setPassword(data.get("password"))
        store.email = data.get("email")
        store.phone = data.get("phone")
        store.address = data.get("address")
        store.logo = img
        store.save()
        return HttpResponseRedirect("/Store/login/")
    return render(request,'Store/register.html')


def logout(request):
    response = HttpResponseRedirect("/Store/login/")
    response.delete_cookie("username")
    return response

def addCommodity(request):
    types = Type.objects.all()
    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        price = data.get("price")
        number = data.get("number")
        datas = data.get("data")
        safe = data.get("safe")
        address = data.get("address")
        types = data.get("types")
        picture = request.FILES.get("picture")
        content = data.get("content")

        c = Commodity()
        c.commodity_name = name
        c.commodity_id = "1234"
        c.commodity_price = price
        c.commodity_number = number
        c.commodity_picture = picture
        c.commodity_data = datas
        c.commodity_safe_data = safe
        c.commodity_address = address
        c.commodity_content = content
        c.delete_flage = "false"
        c.type = Type.objects.get(id = int(types))  #添加外键
        c.save()
        #添加多对多的关系
        store_login_name = request.COOKIES.get("username")  #通过cookie获取店铺的登录名称
        store = Store.objects.get(login_name = store_login_name)  #通过登录名称获取店铺数据
        c.shop.add(store)    #添加数据到商品当中
        c.save()   #再次保存
        return HttpResponseRedirect("/Store/addCommodity/")
    return render(request,"store/addCommodity.html",locals())

def listCommodity(request,type,page):
    page_int = int(page)
    if type == "down":
        commodity_list = Commodity.objects.filter(delete_flage="true").order_by("commodity_data")
    else:
        commodity_list = Commodity.objects.filter(delete_flage="false").order_by("commodity_data")
    paginator = Paginator(commodity_list,10)
    page = paginator.page(page_int)
    if page_int < 4:
        page_range = range(1,6)
    else:
        page_range = paginator.page_range[page_int-3:page_int+2]
    return render(request,"store/listCommodity.html",{"page_data":page,"page_range":page_range,"type":type})

# def addData(request):
    # types = ["海产","肉类","粮油","蛋奶","水果","海外"]
    # for t in types:
    #     ty = Type()
    #     ty.name = t
    #     ty.parent = 0
    #     ty.save()

    # commodity = ["羊肉","大虾","樱桃","鲜奶","大米","牛排"]
    # country = "中国、美国、英国、意大利、日本、俄罗斯、澳大利亚、印度、巴西、埃及、韩国、朝鲜、法国、阿富汗、哥伦比亚、毛里求斯、泰国、巴基斯坦、墨西哥、新西兰、刚果、加拿大、瑞士、爱尔兰、葡萄牙、埃塞俄比亚、西班牙、伊拉克、以色列、挪威、荷兰、捷克、德国、叙利亚、不丹、芬兰、墨西哥".split("、")
    # for i in range(100):
    #     com = Commodity()
    #     c = random.choice(country)
    #     com.commodity_name = c+random.choice(commodity)
    #     com.commodity_id = str(i).zfill(9)
    #     com.commodity_price = random.randint(100,1000)
    #     com.commodity_number = 1000
    #     com.commodity_data = "%s-%s-%s"%(random.randint(1000,1002),random.randint(1,12),random.randint(1,28))
    #     com.commodity_safe_data = 120
    #     com.commodity_address = c
    #     com.commodity_picture = random.choice("store/images/4046.jpg、store/images/777.jpg、store/images/43th.png、store/images/5345.png、store/images/23140.jpg、store/images/25252.jpg".split("、"))  #图片
    #
    #
    #     com.commodity_content = "嘎嘣脆，鸡肉味！"
    #
    #     com.delete_flage = "false"
    #     com.type = Type.objects.get(id = random.randint(1,6))
    #     com.save()
    #     com.shop.add(Store.objects.get(login_name="nx"))
    #     com.save()

    # return HttpResponse("保存成功")

def soldCommodity(request,type,id):
    referer = request.META.get("HTTP_REFERER")
    commodity = Commodity.objects.get(id = int(id))
    if type == "up":
        commodity.delete_flage = "false"
    else:
        commodity.delete_flage = "true"
    commodity.save()
    return HttpResponseRedirect(referer)


def addType(request):
    Types = Type.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        types = request.POST.get("types")
        picture = request.FILES.get("picture")

        t = Type()
        t.name = name
        t.parent = types
        t.picture = picture
        t.save()
    return render(request,"store/addType.html",locals())


def listType(request,type,page,value):
    value=int(value)
    Types = Type.objects.all()
    page_int = int(page)
    if type == "down":
        commodity_list = Commodity.objects.filter(delete_flage="true").order_by("commodity_data")
    else:
        commodity_list = Commodity.objects.filter(delete_flage="false",type=value).order_by("commodity_data")

    paginator = Paginator(commodity_list,10)
    page = paginator.page(page_int)
    if page_int < 4:
        page_range = range(1,6)
    else:
        page_range = paginator.page_range[page_int-3:page_int+2]
    return render(request,"store/listType.html",{"page_data":page,"page_range":page_range,"type":type,"Types":Types})


def order_list(request):
    store = Store.objects.get(login_name=request.COOKIES.get("username"))
    order_list = store.orderresource_set.all()
    return render(request,"store/order_list.html",locals())