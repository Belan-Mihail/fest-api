from rest_framework import serializers
from .models import Wall

class WallSerializer(serializers.ModelSerializer):
        
        owner = serializers.ReadOnlyField(source='owner.username')
        profile = serializers.ReadOnlyField(source='owner.profile')

        def get_is_owner(self, obj):
                request = self.context['request']
                return request.user == obj.owner

        class Meta:
                model = Wall

        fields = [
            'id', 'owner',  'is_owner', 'profile'
        ]