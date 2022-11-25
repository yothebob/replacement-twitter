import json
import jwt

from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from .models import Account, Post, Attachment
from .serializers import AccountSerializer, PostSerializer, AttachmentSerializer
from replacement_twitter.settings import SECRET_KEY
from django.views.decorators.csrf import csrf_exempt



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


    
# JWT
@csrf_exempt
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


@csrf_exempt
def like_item(request):
    json_decoded = json.loads(request.body)
    account = Account.objects.filter().first()
    if account is None:
        return JsonResponse({"error": "Account not found"})
    if json_decoded["item"] == "post":
        post = Post.objects.filter(id=json_decoded["itemKey"]).first()
        if post is not None:
            print(posts.likes)
            post.likes.add(account)
            post.save()
            return JsonResponse({ "success": "post liked" })
    elif json_decoded["item"] == "comment":
        comment = Comment.objects.filter(id=json_decoded["itemKey"]).first()
        if comment is not None:
            comment.likes.add(account)
            comment.save()
            return JsonResponse({ "success": "post liked" })
    return JsonResponse({"error": "Something went wrong..."})        
    

# DEF GET_account_followers(request):
#     userid = request.GET.get("userid","")
#     account = Account.objects.filter(id=userid).first()
#     if account is not None:
#         followers = Account.o
#         return JsonResponse({})
#     else:
#         return JsonResponse({})
    
