import json
import jwt

from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from .models import Account, Post, Attachment
from .serializers import AccountSerializer, PostSerializer, AttachmentSerializer
from replacement_twitter.settings import SECRET_KEY


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


def login_account(request):
    json_decoded = json.loads(request.body)
    found_account = Account.objects.filter(username=json_decoded["username"], password=json_decoded["password"]).first()
    if found_account is not None:
        refresh = jwt.encode({
            "token_type": "refresh",
            "username": found_account.username,
            "password": found_account.password,
            "account_id": found_account.id
        }, SECRET_KEY , algorithm="HS256")
        return JsonResponse({ "refresh": refresh })
    return JsonResponse({"error": "not authenticated"})
    

# def get_account_followers(request):
#     userid = request.GET.get("userid","")
#     account = Account.objects.filter(id=userid).first()
#     if account is not None:
#         followers = Account.o
#         return JsonResponse({})
#     else:
#         return JsonResponse({})
    
