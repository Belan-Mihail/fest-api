from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from profiles.models import Profile


    

class Wall(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wall_owner")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

# def get_recent_items( self):
# return WallItem.objects.all()


def create_wall(sender, instance, created, **kwargs):
    if created:
        Wall.objects.create(owner=instance)

post_save.connect(create_wall, sender=User)
