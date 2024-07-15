from django.shortcuts import render,HttpResponse,redirect

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
            return redirect('/parking/parking/')
    return render(request,"ParkingSpaceForm.html",context)


def ParkingSpaceDeleteView(request,pk):
    obj = ParkingSpace.objects.get(pk=pk)
    obj.delete()
    
    return redirect('/parking/parking/')


def ParkingSpaceCreateView(request):
    context={}
    if request.method=="POST":
        data =request.POST
        number=int(data.get('number'))
        occupied=data.get('occupied')=='on'
        
        if not number<0 and number>10:
            
            ParkingSpace.objects.create(
                name=data.get('name'),
                number=data.get('number'),
                rate=data.get('rate'),
                occupied=occupied
            )
            return redirect('/parking/parking/')
        context={"error":"number should be less then 10 and greater than 0."}
        return render(request,"ParkingSpace.html",context)
    return render(request,"createParkingSpace.html",context)
    