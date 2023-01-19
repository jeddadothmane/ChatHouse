from django.urls import path
from . import views

app_name = "authentification"


urlpatterns = [
    path("logout", views.logout_request, name="logout"),
    path("", views.login_request, name="login"),
    path('home/', views.home, name='home'),
    path('home/checkview', views.checkview, name='checkview'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path('<str:room>/', views.room, name='room'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
]