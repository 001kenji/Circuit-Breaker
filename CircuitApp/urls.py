from django.urls import path,include
from . import views

urlpatterns = [
    path('test1/',views.Test1.as_view(),name='test 1'),
]  
