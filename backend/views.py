import json
import jwt

from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from .models import Account, Post, Attachment, Comment
from .serializers import AccountSerializer, PostSerializer, AttachmentSerializer, CommentSerializer
from replacement_twitter.settings import SECRET_KEY
from django.views.decorators.csrf import csrf_exempt



# ViewSets define the view behavior.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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
    

@csrf_exempt
def add_comment(request):
    # { accountId: 1, body: "test", postId: 1 }
    json_decoded = json.loads(request.body)
    if json_decoded["body"] is None:
        return JsonResponse({"error": "Cannot post empty comment"})
    try:
        account = Account.objects.filter(id=json_decoded["accountId"]).first()
        post = Post.objects.filter(id=json_decoded["postId"]).first()
        if account and post:
            comment = Comment(
                body=json_decoded["body"],
                account=account,
                post=post)
            comment.save()
            serializer = CommentSerializer(comment)
            return JsonResponse({
                "success": "comment added successfully",
                "newComment": serializer.data
            })
        else:
            return JsonResponse({"error": "account or post not found"})
    except: 
        return JsonResponse({"error": "Something went wrong.."})

@csrf_exempt
def create_post(request):
    json_decoded = json.loads(request.body)
    if json_decoded["body"] is None:
        return JsonResponse({"error": "Cannot post empty comment"})
    try:
        account = Account.objects.filter(id=json_decoded["account"]).first()
        new_post = Post(
            account=account,
            title=json_decoded["title"],
            content=json_decoded["content"],
            blog=False,
            image=json_decoded["image"],
            video=json_decoded["video"],
        )
        new_post.save()
        serializer = PostSerializer(new_post)
        return JsonResponse({"success": "post created", "post": serializer.data})
    except:
        return JsonResponse({"error": "Something went wrong.."})
        

    
    # {
    #     "title": "",
    #     "content": "",
    #     "account": null,
    #     "image": "",
    #     "video": "",
    #     "blog": false,
    #     "likes": []
    # }        
