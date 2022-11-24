from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .models import Account, Post, Attachment, Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['account', 'body', 'post','likes' ]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['url', 'title', 'content', 'account', 'blog', 'likes', "comments"]

        
# Serializers define the API representation.
class AccountSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ['username', 'name', 'following', "posts"]

class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attachment
        fields = ['url', 'post', 'name', 'file_path']


# class userPostsSerializer(serializers.HyperlinkedModelSerializer):
    
    
#     class Meta:
#         model = Account
#         fields = [
            
#         ]
