from django.urls import path
from walls import views



urlpatterns = [
    path('walls/', views.WallList.as_view()),
    path('walls/<int:pk>/', views.WallDetail.as_view()),
]
