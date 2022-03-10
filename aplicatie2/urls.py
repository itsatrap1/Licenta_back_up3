from django.urls import path
from aplicatie2 import views

app_name = 'aplicatie2'

urlpatterns = [
    path('new_timesheet', views.newPontaj, name='pontaj'),
    path('stop_timesheet', views.stopTimesheet, name='oprire_pontaj'),
    path('add/', views.CreateCompaniesView.as_view(), name = 'adaugare'),
    path('edit/<int:pk>/', views.UpdateCompaniesView.as_view(), name = 'modificare'),
    path('index/', views.ListCompaniesView.as_view(), name='lista'),
    path('profile/<int:pk>/', views.UpdateProfile.as_view(), name='update_profile'),
    path('new_account/', views.NewAccountView.as_view(), name = 'adauga_utilizator'),
]
