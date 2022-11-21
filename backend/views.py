from django.shortcuts import render
from rest_framework import viewsets
from .models import Account, Post, Attachment
from .serializers import AccountSerializer, PostSerializer, AttachmentSerializer

# ViewSets define the view behavior.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
