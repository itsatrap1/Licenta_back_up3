from django.urls import path

from ski_user_experience.views import CreateInfoView

app_name = "ski_user_experience"

urlpatterns = [
    path('', CreateInfoView.as_view(), name = 'user_questions'),
]
