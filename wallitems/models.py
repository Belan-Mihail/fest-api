from django.db import models
from django.contrib.auth.models import User
from walls.models import Wall


class WallItem(models.Model):
    
    wall = models.ForeignKey(Wall, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wall_item_owner")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)