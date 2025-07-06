from django.urls import path
from .views import index, login, signup, logout, music

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('music/<str:pk>', music, name='music'),
]