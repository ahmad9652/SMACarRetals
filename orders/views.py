from django.shortcuts import render,redirect
from cars.models import Car
from client.models import tennantaddress
from orders.models import Order,CancelOrder
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate,logout
# Create your views here.
def make_order(request,id):
    if request.method=="POST":
        user = request.user
        groups = user.groups.all()
        group=groups.get()
        if group.name == "client": 
            order = Order()
            order.car = Car.objects.get(id=id)
            order.tennant = request.user
            order.from_date = request.POST["from_date"]
            order.to_date = request.POST["to_date"]
            order.price_per_day = order.car.rent_price
            order.price =(datetime.strptime(order.to_date,'%Y-%m-%d')-datetime.strptime(order.from_date,'%Y-%m-%d')).days * order.price_per_day
            order.tennant_address = request.POST["tennant_address"]
            order.city = request.POST["city"]
            order.state = request.POST["state"]
            order.zip = request.POST["zip"]
            if(len(request.FILES['dl'])!=0):
                order.dl = request.FILES["dl"]
                order.car.availablity=False
                order.car.save()
                order.save()
                messages.success(request,"Car is booked")
                return redirect("/")
        else:
            messages.warning(request,"Car is unable to book")
            return redirect("/")
    user = request.user
    add = tennantaddress(tennant=user)
    return render(request,"order.html",{"id":id,"add":add})

def return_car(request):
    if request.method == "POST":
        user = authenticate(username=request.user.username,password=request.POST["password"])
        print(user)
        print(request.user)
        if user is not None:
            car = Car.objects.get(car_number=request.POST["carnumber"])
            if car.owner == request.user:
                order = Order.objects.get(car=car,return_b=False)
                user = request.user
                groups = user.groups.all()
                group = groups.get()
                if group.name == "owner":
                    car.availablity = True
                    car.save()
                    order.return_b=True
                    order.return_date=datetime.now()
                    order.save()
                    messages.success(request,"Car return successfully")
                return redirect("/cars/")
            else:
                messages.error(request,"The Car don't belongs to you")
                return redirect("/")
        else:
            messages.error(request,"Wrong Password!")
            return redirect("/")
    else:
        logout(request)
        messages.error(request,"You are not Authorised")
        return redirect("/")

def order_detail(request,id):
    order=Order.objects.get(id=id)
    return render(request,"orderdetails.html",{"order":order})

def re_rent(request,id):
    if request.method=="POST":
        user = request.user
        groups = user.groups.all()
        group=groups.get()
        if group.name == "client": 
            order = Order()
            order.car = Car.objects.get(id=id)
            if order.car.availablity:
                order.tennant = request.user
                order.from_date = request.POST["from_date"]
                order.to_date = request.POST["to_date"]
                order.price_per_day = order.car.rent_price
                order.price =(datetime.strptime(order.to_date,'%Y-%m-%d')-datetime.strptime(order.from_date,'%Y-%m-%d')).days * order.price_per_day
                order.tennant_address = request.POST["tennant_address"]
                order.city = request.POST["city"]
                order.state = request.POST["state"]
                order.zip = request.POST["zip"]
                if "dl" in request.FILES:
                    if(len(request.FILES['dl'])!=0):
                        order.dl = request.FILES["dl"]
                else:
                    order.dl=user.tennantaddress_set.all().get().dl
                order.car.availablity=False
                order.car.save()
                order.save()
                messages.success(request,"Car is booked")
                return redirect("/")
            else:
                messages.warning(request,"Car is not available")
                return redirect("/cars/")
        else:
            messages.warning(request,"Car is unable to book")
            return redirect("/")
    else:
        user = request.user
        previous_order = Order.objects.get(id=id)
        return render(request,"re_order.html",{"previous_order":previous_order,"user":user})

def cancel_order(request,id):
    order = Order.objects.get(id=id)
    if order.from_date > timezone.now():
        if not(order.cancel_b==True or order.return_b==True):
            order.cancel_b = True
            order.car.availablity=True
            order.car.save()
            order.save()
            cancelorder = CancelOrder(order=order)
            cancelorder.save()
            messages.success(request,"Order has been cancelled successfully ")
            return redirect("/")
        else:
            messages.error(request,"Car is already Returned Or cancelled")
            return redirect("/user/previousorder")
    else:
        messages.error(request ,"You can not cancel the order as order period started already")
        return redirect("/user/previousorder")