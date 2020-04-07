from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path(r'echo/', views.EchoView.as_view(), name='echo'),
    path(r'mailling/', views.MailingServiceView.as_view(), name='mailling'),
    path(r'addtask/', views.AddTaskView.as_view(), name='addtask'),
    path(r'addsecret/', views.AddSecretView.as_view(), name='addsecret'),
]
