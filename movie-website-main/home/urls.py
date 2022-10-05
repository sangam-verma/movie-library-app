from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('details/<str:id>/', views.details, name="details"),
    path('details-saved/<str:idd>/<str:id>/', views.details_saved, name="details_saved"),
    path('add-to-playlist/', views.save_details, name="save_details"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('make-public-playlist/', views.make_public_playlist, name="make_public_playlist"),
    path('make-private-playlist/', views.make_private_playlist, name="make_private_playlist"),
    path('public-playlist/<int:id>/', views.public_playlist, name="public_playlist"),
    path('', views.index, name="index"),
]