from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# 1

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_d9pfdc_pdmycw'
    )
    # add me
    greeting = models.CharField(max_length=25, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


# All good so far, now we need to ensure that a  profile is created every time a user is created.  
# We can do that with a Django  feature called signals.
# You can think of signals as notifications that  get triggered by an event. We can listen for  
# such Model events and have some code, usually a  function, run each time that signal is received.
# In our case, we would want to be notified when a  
# user is created so that a profile can  automatically be created alongside it. 
# Examples of built-in Model signals include:  pre_save, post_save, pre_delete and post_delete.
# So, I’ll import post_save at  the top from Django’s signals.

# 3
# 4 admin
# Now we have to define the create_profile function  before we pass it as an argument. Because we are  
# passing this function to the post_save.connect  method, it requires the following arguments:  
# the sender model, its instance, created  - which is a boolean value of whether or  
# not the instance has just been created, and  kwargs. Inside the create_profile function,  
# if created is True, we’ll create a profile  whose owner is going to be that user.
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)



# 2
# Now I’ll listen for the post_save signal coming  from the User model by calling the connect function. 
# Inside, I’ll pass ‘create_profile’,  which is the function I’d like to run every time  
# and specify User as the model we’re  expecting to receive the signal from.
post_save.connect(create_profile, sender=User)