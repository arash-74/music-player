from django.urls import path

from player import views

app_name = 'music player'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('upload/',views.upload_view,name='upload'),
    path('play/',views.play_view,name='play'),
    path('clear/',views.clear_db,name='clear'),
]