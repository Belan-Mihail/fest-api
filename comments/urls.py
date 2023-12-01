from django.urls import path
from comments import views

# 42 urls. drfapi
# 41

urlpatterns = [
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view())
]