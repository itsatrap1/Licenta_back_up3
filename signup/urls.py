from signup.views import SignUpView
from django.urls import path

app_name = "signup"

urlpatterns = [
    path('new_user/', SignUpView.as_view(), name = 'signup'),

]
