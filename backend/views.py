import json
import jwt
import random
import datetime
import string


from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
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

#TODO switch to jwt auth for everything

@csrf_exempt
def follow_account(request):
    json_decoded = json.loads(request.body)
    account = Account.objects.filter(id=json_decoded["accountId"]).first()
    follow_account = Account.objects.filter(id=json_decoded["followAccountId"]).first()
    if account and follow_account:
        account.following.add(follow_account)
        account.save()
        return JsonResponse({"success": "Account followed"})        
    else:
        return JsonResponse({"error": "Something went wrong.."})        

# JWT
@csrf_exempt
def validate_login(request):
    json_decoded = json.loads(request.body)
    if True:
    # try:
        decoded_jwt = jwt.decode(json_decoded["refresh"],SECRET_KEY, algorithms=["HS256"])
        expire_stamp = datetime.datetime.strptime(decoded_jwt["expire_at"],"%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        if now < expire_stamp:
            print("success")
            return JsonResponse({"success": "authenticated"})
        print("error")
        return JsonResponse({"Error": "not properly authenticated"})
    # except:
    else:
        print("error")
        return JsonResponse({"Error": "not properly authenticated"})

# JWT
@csrf_exempt
def login_account(request):
    json_decoded = json.loads(request.body)
    found_account = Account.objects.filter(username=json_decoded["username"], password=json_decoded["password"]).first()
    expiring = (datetime.datetime.now() + datetime.timedelta(days=1)) 
    if found_account is not None:
        refresh = jwt.encode({
            "token_type": "refresh",
            "username": found_account.username,
            "password": found_account.password,
            "account_id": found_account.id,
            "expire_at": expiring.strftime("%Y-%m-%d %H:%M:%S"),
        }, SECRET_KEY , algorithm="HS256")
        return JsonResponse({ "refresh": refresh , "id": found_account.id})
    return JsonResponse({"error": "not authenticated"})


@csrf_exempt
def like_item(request):
    json_decoded = json.loads(request.body)
    account = Account.objects.filter(id=json_decoded["accountKey"]).first()
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


    
# serperating out because idk?     
# TODO add auth token to auth header
@csrf_exempt
def add_post_image(request):
    print(request.FILES)
    jwt = request.headers.get("Auth", None)
    post_id = request.headers.get("Post", None)
    if jwt is None:
        return JsonResponse({"error": "Something went wrong.."})
    try:
        # decoded_jwt = jwt.decode(json_decoded["refresh"],SECRET_KEY, algorithms=["HS256"])
        data = request.FILES["image"]
        random_str = "".join(random.choice(string.ascii_letters) for i in range(30))
        path = default_storage.save("/var/www/replacement-twitter/account-static/" + random_str, ContentFile(data.read())) 
        post = Post.objects.filter(id=post_id).first()
        post.image = "/var/www/replacement-twitter/account-static/" + random_str
        post.save()
        return JsonResponse({"success": "image added"})
    except:
        return JsonResponse({"error": "Something went wrong.."})
        
    
    
@csrf_exempt
def create_post(request):
    json_decoded = json.loads(request.body)
    if json_decoded["content"] is None:
        return JsonResponse({"error": "Cannot post empty comment"})
    if True:
    # try:
        account = Account.objects.filter(id=json_decoded["account"]).first()
        post_creator = Account.objects.filter(id=json_decoded["postCreator"]).first()
        if account and post_creator:
            new_post = Post(
                account=account,
                post_creator=post_creator,
                title=json_decoded["title"],
                content=json_decoded["content"],
                blog=False,
            )
            new_post.save()
            serializer = PostSerializer(new_post)
            return JsonResponse({"success": "post created", "post": serializer.data})
    # except:
    else:
        return JsonResponse({"error": "Something went wrong.."})
        
    
