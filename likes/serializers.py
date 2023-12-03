from rest_framework import serializers
from django.db import IntegrityError
from .models import Likes

# 45 views
# 44
class LikesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """

    owner = serializers.ReadOnlyField(source='owner.username')


    class Meta:
        model = Likes

        fields = [
            'id', 'created_at', 'owner', 'post'
        ]
    

#     So, let’s get started. Handling duplicates  with the rest framework is pretty easy.  
# All we have to do is define the create  method inside our LikeSerializer  
# to return a complete object instance  based on the validated data.
# Inside a try-except block, I’ll try  to return the newly created like by  
# calling the create method with the validated_data.  
# This create method is on the model serializer  and for that reason I had to call “super()”.
# Anyways, if that throws an IntegrityError, I’ll  raise a serializer validation error and let the  
# users know that this could be happening because  they’re trying to like the same post twice.

# and import from django.db import IntegrityError
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })

