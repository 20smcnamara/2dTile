from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Players/Login', views.AddPlayer, name='AddPlayer'),
    path('Players/Logout/<int:id>', views.RemovePlayer, name='RemovePlayer'),
    path('Players/', views.players, name='players'),
    path('Players/Update/<int:x>/<int:y>/<int:id>', views.UpdatePlayer, name='playerUpdate'),
]