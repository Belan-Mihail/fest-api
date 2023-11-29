from django.urls import path
from profiles import views


# 7
# 8 urls.py drfapi
urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
]