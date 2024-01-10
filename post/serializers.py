from rest_framework import serializers
from .models import Post
from likes.models import Likes

# 25 model
# 24 
class PostSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    # # add i
    profile_content = serializers.ReadOnlyField(source='owner.profile.content')
    # add me
    profile_greeting = serializers.ReadOnlyField(source='owner.profile.greeting')
    likes_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    # 28
#     Finally, we can implement the validation  checks for size, width and height on post images.
# For that, we’ll use the rest  framework’s field level validation methods.  
# They’re called: validate_fieldName,  
# and in our case the field name is ‘image’,  so our method’s name will be validate_image.

# !!! If we follow this naming convention,  this method will be called automatically  
# and validate the uploaded image every  time we create or update a post.
# value == uploded images
    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value
    
#     If they are, we’ll check if they liked the post  we’re trying to retrieve. We’ll filter the Like  
# model where the currently logged in user is the  user who liked the post we’re trying to retrieve.
# If that’s the case, we’ll retrieve  the like_id and None otherwise.
    def get_likes_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Likes.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

# 28-! 
# 29 views

# my owm experement with step 28
    def validate_content(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Content must contain at least 3 characters')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post

        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'created_at', 'updated_at', 'title',
            'content', 'image', 'is_owner', 'image_filter', 'likes_id', 'likes_count', 'comments_count', 'profile_content', 'profile_greeting', 'post_category',
        ]
# 27 add new filter_image field
# 28 up
