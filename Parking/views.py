from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime,timezone
# Create your views here.

from .models import *

def ParkingSpaceView(request):
    context={}
    if request.method=="GET":
        model = ParkingSpace.objects.all()
        context={"model":model}
    return render(request,'parkingspace.html',context=context)


def ParkingSpaceInfoView(request,pk):
    context={}
    obj = ParkingSpace.objects.get(pk=pk)
    context={"obj":obj}
    return render(request,'info.html',context)


def ParkingSpaceChangeView(request,pk):
    context={}
    obj = ParkingSpace.objects.get(pk=pk)
    context={"obj":obj}
    if request.method=="POST":
        # raise Exception(request.POST['name'])
        data = request.POST

        if data:
            # raise Exception(data['name'].value)
            obj.name=data.get('name')
            obj.number=data.get('number')
            obj.rate=data.get('rate')
            obj.occupied=data.get('occupied')=='on'
            obj.save()
            return redirect('parking')
    return render(request,"ParkingSpaceForm.html",context)


def ParkingSpaceDeleteView(request,pk):
    obj = ParkingSpace.objects.get(pk=pk)
    obj.delete()
    
    return redirect('parking')


def ParkingSpaceCreateView(request):
    context={}
    if request.method=="POST":
        data =request.POST
        number=int(data.get('number'))
        occupied=data.get('occupied')=='on'
        
        if  number<0 or number>10:
            context={"error":"number should be less then 10 and greater than 0."}
            return render(request,"createParkingSpace.html",context)
        
        ParkingSpace.objects.create(
            name=data.get('name'),
            number=data.get('number'),
            rate=data.get('rate'),
            occupied=occupied
        )
        return redirect('parking')
    return render(request,"createParkingSpace.html",context)
    

def VehicleDetailsAdd(request):
    
    if request.method=="POST":
        data = request.POST
        Vehicle_info.objects.create(type=data.get('type'),plate_no=data.get('plate_no'))
        return redirect('vehicle_name')
    return render(request,"Vehicle_infoAdd.html")
def VehicleDetailsView(request):
    context={}
    if request.method=="GET":
        obj = Vehicle_info.objects.all()
        context={'obj':obj,}
    return render(request,"VehicleDashBoard.html",context=context)


def VehicleDetailInfo(request,pk):
    obj = Vehicle_info.objects.get(pk=pk)
    context ={"obj":obj}
    return render(request,"VehicleInfo.html",context)

def VehicleDetailEdit(request,pk):
    obj = Vehicle_info.objects.get(pk=pk)
    context ={"obj":obj}
    if request.method=="POST":
        data = request.POST
        obj.type=data.get('type')
        obj.plate_no=data.get('plate_no')
        obj.save()
        return redirect('vehicle_name')
    return render(request,"VehicleEdit.html",context)

def VehicleDetailDelete(request,pk):
    obj = Vehicle_info.objects.get(pk=pk)
    obj.delete()
    
    return redirect('vehicle_name')


def Parking_details(request):
    context ={}
    queryset = ParkingDetails.objects.all().order_by('created_at')
    vehicle_info=Vehicle_info.objects.filter(parked=False)
    parking_space =ParkingSpace.objects.filter(occupied=False)
    context ={"queryset":queryset,"vehicle_info":vehicle_info,"parking_space":parking_space}

    if request.method=="POST":
        data = request.POST
        parking_space_id = data.get('parking_space_user')
        vehicle_info_id=data.get('vehicle_info_user')
        checkout_time=data.get('checkout_time')
        # raise Exception(parking_space,vehicle_info)
        vehicle_obj = Vehicle_info.objects.filter(pk=vehicle_info_id).first()
        parking_obj = ParkingSpace.objects.filter(pk=parking_space_id).first()
        
        
        if parking:=ParkingDetails.objects.filter(vehicle_info=vehicle_info_id).exists():
            # ParkingDetails.objects.filter(vehicle_info=vehicle_info_id).first()
            # Check if parking.checkout_time is timezone-aware
            if parking.checkout_time > timezone.now():
            
                parking.parking_space.occupied=True
                parking.parking_space.save()
                vehicle_obj.parked=True
                vehicle_obj.save()
            else:
                parking.parking_space.occupied=False
                parking.parking_space.save()
                vehicle_obj.parked=False
                vehicle_obj.save()
                # context['error']='Vehicle is already parked'
        
        if parking_obj.occupied:
            context['error']='parking space not available'
        else:
            ParkingDetails.objects.create(parking_space=parking_obj,
                                            vehicle_info=vehicle_obj,
                                           checkout_time=checkout_time)
            
            vehicle_obj.parked=True
            vehicle_obj.save()
            parking_obj.occupied=True
            parking_obj.save()
            context['success']='succesfully created'
            # return render(request,'ParkingDetails.html',context)            
        
    return render(request,'ParkingDetails.html',context)


def home(request):
    return render(request,'home.html')
