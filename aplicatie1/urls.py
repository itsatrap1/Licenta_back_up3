from django.urls import path
from aplicatie1 import views

app_name = 'aplicatie1'

urlpatterns = [
    path('', views.CreateLocationView.as_view(), name='adaugare'),
    path('<int:pk>/update/', views.UpdateLocationView.as_view(), name='modificare'),
    path('list/', views.ListLocationView.as_view(), name='listare'),
    path('delete/<int:pk>/', views.delete_location, name = 'delete'),
]
