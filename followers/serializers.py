from rest_framework import serializers
from django.db import IntegrityError
from .models import Followers

# 49 views
# 48
class FollowersSerializer(serializers.ModelSerializer):
    """
    Serializer for the Followers model
    The create method handles the unique constraint on 'owner' and 'followed'
    """

    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')


    class Meta:
        model = Followers

        fields = [
            'id', 'created_at', 'owner', 'followed', 'followed_name'
        ]
    

# and import from django.db import IntegrityError
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })

