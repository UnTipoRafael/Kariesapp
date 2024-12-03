from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ImagenLocalForm , ImagenDriveForm
from .models import ImagenLocal, ImagenDrive
from django.conf import settings
from ultralytics import YOLO
from PIL import Image
import shutil
# Load a pretrained YOLO11n model
model = YOLO("model/bestv40.pt")

from gdstorage.storage import GoogleDriveStorage



import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.


def index(request):
    #return HttpResponse(request)

    if request.method == "POST":

        form = ImagenLocalForm(request.POST, request.FILES)
        #Drive = ImagenDrive()

        if form.is_valid():
            new=form.save()
            print(new.imagen.name)
            # Define path to the image file
            source = os.path.join(settings.MEDIA_ROOT, new.imagen.name)
            # Run inference on the source
            #predict = model.predict(source, save=True, imgsz=640, conf=0.25, project="media", name="p")
            predict = model.predict(source, imgsz=640, conf=0.25)
            new.ok = predict[0].save(str(new.pk)+".jpeg")
            
            #Drive.name = new.name
            #imagena=open(str(settings.BASE_DIR)+"/"+str(new.pk)+".jpeg")
            #Drive.imagen = new.imagen.name

            storage = GoogleDriveStorage()
            #storage.save(new.imagen.name, imagena)
            #imagena.close()
            with open(source, 'rb') as image_file:
                file_name = storage.save(new.imagen.name, image_file)
                print(f"Imagen guardada en Google Drive con nombre: {file_name}")
            


            shutil.move(str(settings.BASE_DIR)+"/"+str(new.pk)+".jpeg", str(settings.MEDIA_ROOT)+"/predict/"+new.ok.name)
            #imagenb= open(str(settings.MEDIA_ROOT)+"/predict/"+new.ok.name)
            #Drive.ok = "predict/"+new.ok.name
            storage = GoogleDriveStorage()
            with open(str(settings.MEDIA_ROOT)+"/predict/"+new.ok.name, 'rb') as image_file:
                file_name = storage.save("predict/"+new.ok.name, image_file)
                print(f"Imagen guardada en Google Drive con nombre: {file_name}")
        #storage.save("predict/"+new.ok.name, imagenb)
            #imagenb.close()

            #imagenb.close()
            #Drive.save()
            
            new.ok= "predict/"+new.ok.name
            new.save()

  
            


            return redirect('display')
    else:

        form = ImagenLocalForm()

    return render(request, 'index.html', {'form': form})
       
       # form = ImagenForm()
       # return render(request, 'hotel_image_form.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')

def display(request):

    if request.method == 'GET':
        # getting all the objects of hotel.
        local = ImagenLocal.objects.all().values()
        #drive = ImagenDrive.objects.all().values()

        storage = GoogleDriveStorage()
        directorios, archivos = storage.listdir('images')
        directorios, archivosPredict = storage.listdir('predict')
        a=[]
        for item in archivos:
            id=storage.url(item).replace("https://drive.google.com/uc?", "")
            id=id.replace("=/", "")
            id=id.replace("id=", "")
            id=id.replace("&export=", "")
            id=id.replace("download", "")
            a.append(id)
        for item in archivosPredict:
            id=storage.url(item).replace("https://drive.google.com/uc?", "")
            id=id.replace("=/", "")
            id=id.replace("id=", "")
            id=id.replace("&export=", "")
            id=id.replace("download", "")
            a.append(id)

        # getting all the objects of hotel.
        #aa = ImagenDrive.objects.all()
        #aa = aa.values()

        return render(request, 'display.html', {'drive': a, 'local': local})
    
def drive(request):
    if request.method == 'GET':
        storage = GoogleDriveStorage()
        directorios, archivos = storage.listdir('images')
        a=[]
        for item in archivos:
            id=storage.url(item).replace("https://drive.google.com/uc?", "")
            id=id.replace("=/", "")
            id=id.replace("id=", "")
            id=id.replace("&export=", "")
            id=id.replace("download", "")
            a.append(id)
        # getting all the objects of hotel.
        aa = ImagenDrive.objects.all()
        aa = aa.values()
        return render(request, 'drive.html', {'images': a})

def process(request):
    if request.method == 'GET':
        # getting all the objects of hotel.
        aa = ImagenLocal.objects.all()
        aa = aa.values()
        return render(request, 'display.html', {'images': aa})