from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment

# 40 views
# 39 and migrations
class CommentSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    # post = serializers.ReadOnlyField(source='owner.post.id') dont need!
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    # update data formatting and from django.contrib.humanize.templatetags.humanize import naturaltime
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

# update data formatting
    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

# update data formatting
    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)


    def validate_content(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Content must contain at least 6 characters')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Comment

        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'created_at', 'updated_at', 'post',
            'content', 'is_owner', 
        ]

# When editing a Comment, it should always be associated with the same Post. 
# Therefore, we should create an additional serializer which automatically references
#  the Post Id which the comment is associated with.

class CommentDetailSerializer(CommentSerializer):
# As there is a direct Foreign Key link, 'post', between Comment and Post, 
# we can leave out the User Instance from our source dot notation.
    post = serializers.ReadOnlyField(source='post.id') 