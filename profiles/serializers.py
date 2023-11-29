from rest_framework import serializers
from .models import Profile

# 9
# 10 views.py
class ProfileSerializer(serializers.ModelSerializer):
#     We’ll create a ProfileSerializer class and inherit  from ModelSerializer. We’ll specify ‘owner’ as a  
# ReadOnlyField so that it can’t be edited. We’ll  also populate it with the owner's username.
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile

#         In the Meta class, we’ll point to our Profile  model and specify the fields we’d like to  
# include in the response.
        # fields = '__all__'
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image'
        ]

# Please note, that when extending Django's model class using models.models,
# the id field is created automatically without us having to write it ourselves.
# If we want it to be included in the response, we have to add it to the serializer's field array.
# Now, let's add our serializer to our views.py file.