from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .models import Account, Post, Attachment

# Serializers define the API representation.
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'username', 'name' ]

class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attachment
        fields = ['url', 'post', 'name', 'file_path']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['url', 'title', 'content', 'account', 'blog' ]

