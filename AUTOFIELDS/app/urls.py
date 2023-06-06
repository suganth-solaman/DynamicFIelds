from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_employee, name='create'),
    path('dynamic', views.dynamic, name='dynamic'),
    path('view/<int:pk>', views.view, name='view'),
]
