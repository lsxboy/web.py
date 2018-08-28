from django.shortcuts import render, redirect
from axf.models import SlideShow, MainDescription, Product, CategorieGroup, ChildGroup, User,Address,Cart,Order
from django.http import JsonResponse
import multiprocessing


def add(flag,cart,product,ppid):
    if flag == '1':
        print('--------------用户增加商品线程启动')
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
        print('-----------------用户减少商品线程启动')
        if cart.num == 0:
            print('-------------没有购此商品无需减少')
            return JsonResponse({'reload': True})
        cart.num = str(int(cart.num) - 1)
        pdt = Product.objects.get(pk=ppid)
        pdt.storeNums = str(int(pdt.storeNums) + 1)
        pdt.save()
        cart.save()
        print('------------成功减去购物车数量')
        return JsonResponse({'Succeed': cart.num})


def yibu(flag,cart,product,ppid):
    print('------主进程启动')
    p = multiprocessing.Process(target=add,args=(flag,cart,product,ppid))
    p.start()
    p.join()
    print('----------主进程结束')








