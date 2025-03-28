"""
URL configuration for e_waste project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'e_waste'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('customer/', include('customer.urls')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('driver/', include('driver.urls')),
    path('operator/', include('e_waste_operator.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    # path('', include('customer.urls')),  # Set customer app as the root URL
    path('', views.landing, name='landing'),
]
