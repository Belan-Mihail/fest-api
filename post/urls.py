from django.urls import path
from post import views

# 31 urls drfapi
# 30

urlpatterns = [
    path('posts/', views.PostList.as_view()),

    # 36 view delete method postdetail
    # 35
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    # 35-!
]