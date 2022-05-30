from django.urls import path
from aplicatie2 import views
from aplicatie2.views import HomeView, ProfileView, AddRatingView  # , VisitedListView

app_name = 'aplicatie2'

urlpatterns = [

    # path('profile/<int:pk>/', views.UpdateProfile.as_view(), name='update_profile'),
    # path('new_account/', views.NewAccountView.as_view(), name = 'adauga_utilizator'),
    # path('add/', views.CreateResortView.as_view(), name = 'adaugare'),
    # path('edit/<int:pk>/', views.UpdateResortView.as_view(), name = 'modificare'),
    path('', HomeView.as_view(), name = 'home'),
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('rating/', AddRatingView.as_view(), name = 'rating')
]
