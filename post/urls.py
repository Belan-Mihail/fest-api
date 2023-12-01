from django.urls import path
from post import views

# 31 urls drfapi
# 30

urlpatterns = [
    path('posts/', views.PostList.as_view()),
]