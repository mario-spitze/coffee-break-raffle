from django.conf.urls import url, include
from django.urls import path

from . import views
app_name = 'raffle'
urlpatterns = [
    path('', views.index, name='index'),
    path('createRaffle/', views.createRaffle, name='createRaffle'),
    path('listRaffle/<int:id>', views.ListRaffleView.as_view(), name='listRaffle'),
]