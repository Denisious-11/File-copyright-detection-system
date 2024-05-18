from django.shortcuts import render
from .models import *
import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db.models import Count
import re
import os
import cv2
from datetime import datetime
import shutil
from datetime import date
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
from .perform_crypto import *

# Create your views here.

@never_cache
def show_index(request):
    return render(request, "login.html", {})


@never_cache
def logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    return render(request,'login.html')

@never_cache
def show_register(request):
	return render(request, "register.html", {})

@never_cache
def register(request):
	username = request.POST.get("username")
	password = request.POST.get("password")
	phone = request.POST.get("phone")
	email = request.POST.get("email")

	obj1=Users.objects.filter(username=username)
	c=obj1.count()
	if c==1:
		return HttpResponse("<script>alert('Username Already Taken');window.location.href='/show_register/'</script>")

	else:
		obj2=Users(username=username,password=password,phone=phone,email=email)
		obj2.save()

		return HttpResponse("<script>alert('Registered Successfully');window.location.href='/show_index/'</script>")


def check_login(request):
	username = request.POST.get("username")
	password = request.POST.get("password")

	print(username)
	print(password)

	d = Users.objects.filter(username=username, password=password)
	c = d.count()
	if c == 1:
		d2 = Users.objects.get(username=username, password=password)
		request.session["uid"] = d2.u_id
		request.session["username"]=d2.username
		return HttpResponse("<script>alert('Login Successful');window.location.href='/show_home_user/'</script>")
	else:
		return HttpResponse("<script>alert('Invalid Credentials');window.location.href='/show_index/'</script>")

@never_cache
###############ADMIN START
def show_home_user(request):
	if 'uid' in request.session:
		get_username=request.session["username"]
		return render(request,'home_user.html',{"username":get_username}) 
	else:
		return render(request,'login.html')

@never_cache
def display_upload_file(request):
	if 'uid' in request.session:

		return render(request,'display_upload_file.html',{}) 
	else:
		return render(request,'login.html')

def upload_file(request):
	try:
		username=request.session["username"]
		
		f2= request.FILES["file"]
		file_name=str(f2.name)

		print("f2: ",f2)
		print("file_name: ",file_name)

		if Files.objects.filter(file_name=file_name,username=username).exists():
			return HttpResponse("<script>alert('File with this name already exists');window.location.href='/display_upload_file/'</script>")

		else:

			fs10 = FileSystemStorage("app/static/Temp_Files/")#%username
			fs10.save(file_name, f2)

			len_decoded,decoded=data_decode("app/static/Temp_Files/"+file_name)

			if len(decoded)!=0:
				if os.path.isfile("app/static/Temp_Files/"+file_name):
					os.remove("app/static/Temp_Files/"+file_name)

				if decoded==username:
					return HttpResponse("<script>alert('You already Uploaded this file');window.location.href='/display_upload_file/'</script>")
				else:
					return HttpResponse("<script>alert('Copyright Detected!!!, Patent Author : %s');window.location.href='/display_upload_file/'</script>"%(decoded))

			else:
				get_msg=data_encode("app/static/Temp_Files/"+file_name,username)

				if get_msg=='[Alert]: Your file contents are minimum,Please add more contents in file':
					if os.path.isfile("app/static/Temp_Files/"+file_name):
						os.remove("app/static/Temp_Files/"+file_name)
					return HttpResponse("<script>alert('[Alert]: Your file contents are minimum,Please add more contents in file');window.location.href='/display_upload_file/'</script>")
				else:
					if os.path.isfile("app/static/Temp_Files/"+file_name):
						os.remove("app/static/Temp_Files/"+file_name)

					now = datetime.now()
					time = now.strftime("%H:%M:%S")
					print("Current Time =", time)

					today = date.today()
					current_date = today.strftime("%d/%m/%Y")
					print("date =",current_date)


					obj1=Files(file_name=file_name,username=username,c_date=current_date,c_time=time)
					obj1.save()

			return HttpResponse("<script>alert('File Uploaded Successfully');window.location.href='/display_upload_file/'</script>")
	except:
		return HttpResponse("<script>alert('Your file contains suspicious items, Choose other file');window.location.href='/display_upload_file/'</script>")
@never_cache
def view_files_user(request):
	if 'uid' in request.session:
		req_list=Files.objects.all()
		return render(request,'view_files_user.html',{'req': req_list}) 
	else:
		return render(request,'login.html')

def download(request):
	filename=request.POST.get("file_name")
	get_username=request.session["username"]
	file_uname=request.POST.get("username")
	if True:
        
		file1_path = "app/static/Files/"+file_uname+"/"+filename
		print(os.path.exists(file1_path))
		print(file1_path)

		src_path = "app/static/Files/"+file_uname+"/"+filename
		dir_="app/static/Downloaded_Files/"+get_username
		if not os.path.exists(dir_):
			os.mkdir(dir_)
		dst_path = "app/static/Downloaded_Files/"+get_username+"/"+filename
		shutil.copy(src_path, dst_path)

		if os.path.exists(file1_path):
			with open(file1_path, 'rb') as fh:
				response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
				response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file1_path)
				return response
		raise HttpResponse("<script>alert('File does not exists');window.location.href='/view_files_user/'</script>")
	# return HttpResponse("<script>alert('File Downloaded Successfully to Download_Files folder');window.location.href='/view_files_user/'</script>")


@never_cache
def refresh(request):
	try:
		Files.objects.all().delete()
		dir_path1="app/static/Temp_Files/"
		dir_path2="app/static/Files/"
		dir_path3="app/static/Downloaded_Files/"

		for files in os.listdir(dir_path1):
		    path = os.path.join(dir_path1, files)
		    try:
		        shutil.rmtree(path)
		    except OSError:
		        os.remove(path)

		for files1 in os.listdir(dir_path2):
		    path1 = os.path.join(dir_path2, files1)
		    try:
		        shutil.rmtree(path1)
		    except OSError:
		        os.remove(path1)

		for files3 in os.listdir(dir_path3):
		    path3 = os.path.join(dir_path3, files3)
		    try:
		        shutil.rmtree(path3)
		    except OSError:
		        os.remove(path3)


		return HttpResponse("<script>alert('Refreshed Successfully');window.location.href='/show_home_user/'</script>")
	except:
		return HttpResponse("<script>alert('Something happend');window.location.href='/show_home_user/'</script>")

