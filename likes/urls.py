from django.urls import path
from likes import views

# 47 urls. drfapi
# 46

urlpatterns = [
    path('likes/', views.LikesList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view())
]