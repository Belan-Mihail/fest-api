from django.urls import path
from wallitems import views



urlpatterns = [
    path('wallitems/', views.WallItemList.as_view()),
    path('wallitems/<int:pk>/', views.WallItemDetail.as_view()),
]
