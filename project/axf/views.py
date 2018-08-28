from django.shortcuts import render, redirect
from axf.models import SlideShow, MainDescription, Product, CategorieGroup, ChildGroup, User,Address,Cart,Order
from django.http import JsonResponse
import uuid
#序列化用户信息返回前端
from axf.serializers import UserSerializer
#消息发送
from axf.seedmasege import sendmessage
from axf.sendemail import sendemail
#反序列化解析
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from django.http import HttpResponse
from django.contrib.auth import logout
from axf.md5_auth import encryption
from axf.server_auth import Server_auth
from axf.find_user_data import find_user_data
import multiprocessing
from axf.course import yibu
from django.contrib.sessions.models import Session






def home(request):
    is_login = request.session.get('islogin',False)
    if is_login:
        #获取轮播图数据
        slideList = SlideShow.objects.all()
        #获取5大模块数据
        mainList = MainDescription.objects.all()
        for item in mainList:
            products = Product.objects.filter(categoryId=item.categoryId)
            item.product1 = products.get(productId=item.product1)
            item.product2 = products.get(productId=item.product2)
            item.product3 = products.get(productId=item.product3)
        return render(request, "home/home.html", {"slideList":slideList, "mainList":mainList})
    else:
        return redirect('/login/')

def market(request, gid, cid, sid):

    # user_data = request.session.get(request.COOKIES.get('token'))
    # try:
    #     user_motto,phone = find_user_data(user_data)
    # except:
    #     pass
    print('---------------------maret页面token信息',request.COOKIES.get('token'))
    leftCategorieList = CategorieGroup.objects.all()
    #获取分组商品的信息
    products = Product.objects.filter(categoryId=gid)
    #获取子类数据
    if cid != "0":
        products = products.filter(childId=cid)
    #排序
    if sid == "1":
        # products = products.order_by()
        pass
    elif sid == "2":
        products = products.order_by("price")
    elif sid == "3":
        products = products.order_by("-price")
    #获取子组信
    childs = ChildGroup.objects.filter(categorie__categorieId=gid)
    return render(request, "market/market.html", {"leftCategorieList":leftCategorieList, "products":products, "childs":childs})

def mine(request):
    print('-------------当前token',request.COOKIES.get('token'))
    try:
        user_motto,phone = find_user_data(request.session.get(request.COOKIES.get('token')))
        return render(request, "mine/mine.html", {"phone": phone})
    except:
        return render(request, "mine/mine.html")


def login(request):

    if request.method == "GET":
        #get请求是要登录
        return render(request,"mine/login.html")
    else:
        #获取表单信息
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        try:
            #找到用户
            user = User.objects.get(pk=phone)
        except:
            return redirect('/login/')
        #判断密码是个否正确
        if encryption(password) == user.passwd:
            token =str(uuid.uuid4())
            user.token = token
            user.save()
            data = {
                'userid':user.phoneNum,
                'user_motto':user.motto
            }
            # 保持用户登录状态
            request.session[token] = str(data)
            request.session['islogin'] = True
            response = render(request,"mine/mine.html/",{'phone':user.phoneNum})
            response.set_cookie("token",token)
            print('-----------------------------设置的token',token)
            print('-----------------------------设置的登录状态',request.session.get("islogin"))
            print('-----------------------------设置的session',request.session.get(token))
            return response
        # else:
        #     print('-----------------------密码认证不通过')
        return render(request,'mine/login.html')


def particulars(request):
    status = request.COOKIES.get('islogin')
    if status == 'True':
        print('--------------status？', status)
        user_motto,phone = find_user_data(request.session.get(request.COOKIES.get('token')))
        users = User.objects.get(phoneNum=phone)
        return render(request,'mine/particulars.html',{'users':users})
    else:
        return render(request,'mine/login.html')

def register(request):
    if request.method == "GET":
        return render(request, 'mine/register.html')
    if request.is_ajax():
        try:
            #如果用户发送AJAX请求，但是有此用户，将页面告诉前端用户已经存在
            #如果没有拿到用户信息，证明是新用户，将会走下面分支，完成验证发送
            phone = request.POST.get('phone')
            User.objects.get(pk=phone)
            return JsonResponse({'repetition':1})
        except:
            print('----------------------------新用户注册')
            import random
            base_str = "1234567890"
            auth_code = ''
            for i in range(0, 6):
                auth_code += base_str[(random.randrange(0, len(base_str)))]
            phone = request.POST.get('phone')
            respones = JsonResponse("ok", safe=False)
            respones.set_cookie('auth_code',auth_code)
            print('-----------------发送的验证码:',auth_code,'手机号---',phone)
            request.session['phone'] = phone
            # 短信发送
            # sendmessage(phone,auth_code)
            # # 邮件发送
            # to = '1024801140@qq.com'
            # sendemail(to, session_auth_code)
            return respones
    else:
        #首先将密码加密
        password = encryption(request.POST.get('password'))
        phone = request.POST.get('phone')
        auth_code = request.POST.get('auth_code')
        motto = '欢乐购第一批会员'
        print('-----------表单手机号',phone,'验证码',auth_code)
        if str(phone) == str(request.session.get('phone')):
            print('手机号验证通过')
            if auth_code == request.COOKIES.get('auth_code'):
                print('验证码验证通过')
                token = uuid.uuid4()
                print('-------------------------token',token)
                print('----------------用户信息保存前')
                user = User.objects.create(phoneNum=phone,passwd=password,token=token,motto=motto)
                user.save()
                print('----------------用户信息保存后')
                user_data = {
                    'user_phone':phone,
                    'user_motto':motto,
                }
                request.session[str(token)]=str(user_data)
                respones = render(request, 'mine/mine.html', {"phone": phone})
                respones.set_cookie('token',str(token))

                return respones
            else:
                print('验证码验证失败')
                return redirect('/register/')
        else:
            print('-------session手机号验证失败')
            return render(request,'mine/register.html')

def xiangqing(request,gid, cid, sid,pid):
    IS_LOGIN = request.session.get("islogin", False)
    if IS_LOGIN:
        try:
            print('-----------------',request.COOKIES.get('token'))
            user_motto, phone = find_user_data(request.session.get(str(request.COOKIES.get('token'))))
            carts = Cart.objects.filter(user__phoneNum=phone)
            market = request.get_host()+ ":8000/market/{}/{}/".format(gid,cid)
            url_pid = request.get_full_path().rsplit("/")[::-1][1]
            pid_obj = Product.objects.filter(productId=url_pid).first()
            print('---------------Islogin')
            return render(request, "market/xiangqing.html", {"pid_obj": pid_obj, "market": market,'carts':carts})
        except:
            print('---------------Nologin')
            market = request.get_host() + ":8000/market/{}/{}/".format(gid, cid)
            url_pid = request.get_full_path().rsplit("/")[::-1][1]
            pid_obj = Product.objects.filter(productId=url_pid).first()
            return render(request, "market/xiangqing.html",{"pid_obj": pid_obj, "market": market})
    else:
        return redirect('/login/')

def dizhi(request):
    IS_LOGIN = request.session.get("islogin", False)
    if IS_LOGIN:
        user_motto, phone = find_user_data(request.session.get(str(request.COOKIES.get('token'))))
        addresses = Address.objects.filter(user__phoneNum = phone)
        return render(request,"mine/dizhi.html",{"addresses":addresses})
    else:
        return redirect('/login/')

def add(request):
    IS_LOGIN = request.session.get("islogin", False)
    user_motto, phone = find_user_data(request.session.get(str(request.COOKIES.get('token'))))
    if IS_LOGIN and phone:
        if request.method == "GET":
            return render(request,'mine/add.html')
        else:
            username = request.POST.get("name")
            phone = request.POST.get("phoneNum")
            sex = request.POST.get("sex")
            if sex == "男":
                sex = 0
            sex = 1
            postCode = request.POST.get("postCode")
            province = request.POST.get("province")
            city = request.POST.get("city")
            county = request.POST.get("county")
            street = request.POST.get("street")
            detailAddress = str(province)+str(city)+str(county)+str(street)
            user1 = User.objects.get(phoneNum=phone)
            saves = Address.create(name=username,sex=sex,phoneNum=phone,postCode=postCode,address=detailAddress,province=province,city=city,county=county,street=street,detailAddress=detailAddress,user=user1)
            saves.save()
            return redirect("/dizhi/")
    return render(request,"mine/add.html")

def update(request):
    return render(request,"mine/update.html")


def userlist(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method == "POST":
        #首先将request的信息反向解析
        content = JSONRenderer().render(request.POST)
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        #将信息传进序列化类
        serializer = UserSerializer(data=data)
        #判断数是否正确
        if serializer.is_valid():
            serializer.save()
            #成功后返回向后台提交的数据，表示成功
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

def users(request,pk):
    try:
        users = User.objects.get(pk=pk)
    except User.DoesNotExist as e:
        return HttpResponse(status=404)
    if request.method == "GET":
        serializer = UserSerializer(users)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        content = JSONRenderer().render(request.POST)
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = UserSerializer(users,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        users.delete()
        return HttpResponse(status=204)

def order_form(request):
    return render(request,'mine/order_form.html')

def changecart(request,flag):
    tokenValue = request.COOKIES.get('token')
    print('----------------购物车页面用户token',tokenValue)

    try:
        user_motto,phone = find_user_data(request.session.get(str(tokenValue)))
    except:
        print('------------通过token获取用户信息出错')
        return JsonResponse({'login':True})
    if user_motto and phone:
        print('--------------第一阶段认证通过')
        try:
            user = User.objects.get(token=tokenValue)
            print('--------------第二阶段认证通过')
            print('获取当前请浏览器的token---------------',tokenValue)
            print('获取当前请求的用户phone------------------', phone)
        except:
            print('--------------------用户Token异常',tokenValue)
            return JsonResponse({'Error': True})

        pid = request.POST.get("pid")
        gid = request.POST.get("gid")
        ppid = request.POST.get("ppid")
        product = Product.objects.filter(categoryId=gid).get(productId=pid)
        try:
            # 根据用户手机号码，试图找到收货地址
            user_motto, phone = find_user_data(request.session.get(str(tokenValue)))
            Address.objects.get(phoneNum=phone)
            print('用户有收货地址')
        except:
            # 如果没有找到用户地址，提醒用户去添加地址
            print('-------------用户没有收货地址')
            return JsonResponse({"None": 3})
        try:
            # 如果没报错，证明用户购买过商品   定位用户
            user_motto, phone = find_user_data(request.session.get(str(request.COOKIES.get('token'))))
            cart = Cart.objects.filter(user__phoneNum=phone).get(product__id=ppid)
            # yibu(flag, cart, product, ppid)
            if flag == '1':
                print('--------------用户增加商品')
                if int(product.storeNums) == 0:
                    print('------------商品库存为空')
                    return JsonResponse({'Null': True})
                else:
                    cart.num = str(int(cart.num) + 1)
                    pdt = Product.objects.get(id=ppid)
                    pdt.storeNums = str(int(pdt.storeNums) - 1)
                    pdt.save()
                    cart.save()
                    print('------------增加购物车的数量')
                    return JsonResponse({'Succeed': cart.num})
            else:
                if cart.num == 0:
                    # cart.delete()

                    return JsonResponse({'reload': True})
                cart.num = str(int(cart.num) - 1)
                pdt = Product.objects.get(pk=ppid)
                pdt.storeNums = str(int(pdt.storeNums) + 1)
                pdt.save()
                cart.save()
                print('------------去掉购物车的数量')
                return JsonResponse({'Succeed': cart.num})
        except:
            print('--------------没有找到用户的购物车订单')
            orderId = str(uuid.uuid4())
            # 获取用户的           收货地址
            address = Address.objects.get(user__phoneNum=phone)
            # 创建                订单数据
            order = Order.create(orderId, user, address, product.price)
            # 保存数据
            order.save()
            # 再次找到            订单对象
            oder = Order.orders2.get(pk=orderId)
            # 创建                 购物车数据
            cart = Cart.create(user=user, product=product, order=oder, num = 1)
            cart.save()
            product.storeNums = str(int(product.storeNums) - 1)
            product.save()
            # 告诉客户端添加成功
            print('----------------新用户/新商品数据增加完毕')
            return JsonResponse({'Succeed': cart.num})
    else:
        print('用户身份认证失败')
        return render(request, 'mine/login.html')

def quit(request):
    response = render(request, 'mine/mine.html')
    token = request.COOKIES.get('token')
    try:
        del request.session[token]
    except:
        pass
    print('---------session已经清空',request.session.get(token))
    response.set_cookie('token', None)
    response.set_cookie('autho_code', None)
    return response

def cart(request):
    sessionid = request.COOKIES.get('token')

    if sessionid and request.session.get('islogin'):
        print('------------------------------sessionid', sessionid)
        try:
            user_motto, phone = find_user_data(request.session.get(sessionid))
            print('--------------------------------------2购物车手机号', phone)
            carts = Cart.objects.filter(user__phoneNum=phone)
            print('正常状态录状态进入')
            return render(request, "cart/cart.html", {"carts": carts})
        except:
            print('------------------没有token值')
            return render(request,'cart/cart.html')
    print('未登录状态进入')
    return render(request,'cart/cart.html')


def changecart2(request,flag):
    if request.COOKIES.get('token'):
        pid = request.POST.get('pid')
        uesr_motto,phone = find_user_data(request.session.get(str(request.COOKIES.get('token'))))
        #首先找到商品对象
        print('--------------------------商品id',pid)
        print('--------------------------用户手机号',phone)
        print('--------------------------购买状态',flag)
        product = Product.objects.get(id=pid)

        #在此找到购物车对象

        cart = Cart.objects.filter(user__phoneNum=phone).get(product_id=pid)
        if flag == '1':
            print('---------------------------进入添加状态？')
            if int(product.storeNums) < int(cart.num):
                # print('---------------------------库存不足？',cart.num,product.storeNums)
                return JsonResponse({'Null': True})
            else:
                # print('--------------------------进入数据更改分支？', cart.num, product.storeNums)
                cart.num = str(int(cart.num) + 1)
                pdt = Product.objects.get(id=pid)
                pdt.storeNums = str(int(pdt.storeNums) - 1)
                pdt.save()
                cart.save()
                print('--------------------------数据修改完毕!', cart.num, product.storeNums)
                print('_-'*50)
                return JsonResponse({'Num': cart.num})
        else:
            if cart.num == 1:
                # print('---------------------------进入删除Cart状态？')
                cart.delete()
                return JsonResponse({"Del":True})
            else:
                print('---------------------------进入删除状态？')
                # print('--------------------------数据修改前!', cart.num, product.storeNums)
                cart.num = str(int(cart.num) - 1)
                pdt = Product.objects.get(id=pid)
                pdt.storeNums = str(int(pdt.storeNums) + 1)
                pdt.save()
                cart.save()
                print('--------------------------数据修改完毕!', cart.num, product.storeNums)
                print('_-' * 50)
                return JsonResponse({'Num': cart.num})
    else:
        return redirect('login')


def index(request):
    return render(request,'home/index.html')
