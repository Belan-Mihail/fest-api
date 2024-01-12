from django.db import models
from django.contrib.auth.models import User



class WallItem(models.Model):
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wall_item_owner")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)