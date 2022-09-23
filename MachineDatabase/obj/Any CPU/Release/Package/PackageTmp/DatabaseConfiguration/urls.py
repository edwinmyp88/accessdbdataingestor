from django.urls import path
from DatabaseConfiguration import views

urlpatterns = [
    path('', views.index),
    path('refresh/', views.refresh),
    path('active/<int:id>/', views.active),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete)
]
