from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .models import Account, Post, Attachment, Comment
from replacement_twitter.settings import BASE_DIR



class CommentSerializer(serializers.ModelSerializer):
    account_username = serializers.SerializerMethodField()
    account_comment_color = serializers.SerializerMethodField()
    
    def get_account_username(self, obj):
        return obj.account.username

    def get_account_comment_color(self, obj):
        return obj.account.post_color

    class Meta:
        model = Comment
        fields = ["id",'account', 'account_username', 'account_comment_color', 'body', 'post','likes' ]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    account_username = serializers.SerializerMethodField()
    account_post_color = serializers.SerializerMethodField()
    stripped_video = serializers.SerializerMethodField()
    stripped_image = serializers.SerializerMethodField()

    def get_account_username(self, obj):
        return obj.account.username

    def get_stripped_video(self, obj):
        if str(obj.video) != "":
            return str(obj.video).replace(str(BASE_DIR), "")
        return ""

    def get_stripped_image(self, obj):
        if str(obj.image) != "":
            return str(obj.image).replace(str(BASE_DIR), "")
        return ""

    def get_account_post_color(self, obj):
        return obj.account.post_color

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'account', "stripped_image", "stripped_video", 'account_username', 'account_post_color', 'blog', 'likes', "comments"]

        
# Serializers define the API representation.
class AccountSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ["id",'username', 'name', 'following', "posts"]

class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attachment
        fields = ['url', 'post', 'name', 'file_path']


# class userPostsSerializer(serializers.HyperlinkedModelSerializer):
    
    
#     class Meta:
#         model = Account
#         fields = [
            
#         ]
