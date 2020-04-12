"""coviddb URL Configuration

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
from django.urls import path
from django.contrib import admin
import coviddb.views

urlpatterns = [
    url(r'^$', coviddb.views.index, name='index'),

    path('analytics/num_patients', coviddb.views.num_patients, name='num_patients'),

    path('data/<str:state>/', coviddb.views.data, name='data_list'),
    path('data/<str:state>/<int:id>', coviddb.views.detail, name='data_detail'),

    path('about', coviddb.views.about, name='about'),
    path('info', coviddb.views.info, name='info'),
    path('about_data', coviddb.views.about_data, name='about_data'),
    path('data_link', coviddb.views.data_link, name='data_link'),

    url(r'^manage/', admin.site.urls),
]
