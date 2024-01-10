from rest_framework import serializers
from .models import Profile
from followers.models import Followers

# 9
# 10 views.py
class ProfileSerializer(serializers.ModelSerializer):
#     We’ll create a ProfileSerializer class and inherit  from ModelSerializer. We’ll specify ‘owner’ as a  
# ReadOnlyField so that it can’t be edited. We’ll  also populate it with the owner's username.

# The User and Profile tables are connected  through the owner OneToOne field.  
# By default, the owner field always  returns the user’s id value.
# For readability’s sake, however,  every time we fetch a profile,  
# it makes sense to overwrite this default behaviour  and retrieve the user’s username instead.  
# To access this field, we use dot notation.
    owner = serializers.ReadOnlyField(source='owner.username')
    # 20
    # 21 below
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
        # так сделано (передается контекст который вставлен во все методы сеиалаз в представдениях
        # ) так как без контекста request.user это будет любой текущий юзе а не владелец профиля
        #  и проверка request.user == obj.owner будет работать не корректно

    # my owm experement with step 28
    def validate_content(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Content must contain at least 3 characters')
        return value
    

    def get_following_id(self, obj):
        # get current user
        user = self.context['request'].user
        # check if user.is_authenticated
        if user.is_authenticated:
            # Then I will check if the logged in user  is following any of the other profiles.  
            # To do this I will filter the Follower object.
            # If the logged in user is following this  profile an instance will be returned.
            # If the logged in user is not following  this profile, None will be returned.
            following = Followers.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            print(following)
            return following.id if following else None
        return None


    class Meta:
        model = Profile

#         In the Meta class, we’ll point to our Profile  model and specify the fields we’d like to  
# include in the response.
        # fields = '__all__'
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id', 'posts_count',
            'followers_count', 'following_count', 'greeting'
            # 21 add 'is_owner'
        ]

# Please note, that when extending Django's model class using models.models,
# the id field is created automatically without us having to write it ourselves.
# If we want it to be included in the response, we have to add it to the serializer's field array.
# Now, let's add our serializer to our views.py file.

# 22 new app post
# 23 model.post