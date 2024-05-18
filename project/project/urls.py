"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$',show_index),
    url(r'^show_index', show_index, name="show_index"),
    url(r'^check_login', check_login, name="check_login"),
    url(r'^logout',logout,name="logout"),
    url(r'^show_register',show_register,name="show_register"),
    url(r'^register',register,name="register"),
    ##########login end

    ################Admin start
    url(r'^show_home_user',show_home_user,name="show_home_user"),
    url(r'^display_upload_file',display_upload_file,name="display_upload_file"),
    url(r'^upload_file',upload_file,name="upload_file"),
    url(r'^view_files_user',view_files_user,name="view_files_user"),
    url(r'^download',download,name="download"),
    url(r'^refresh',refresh,name="refresh"),

]
