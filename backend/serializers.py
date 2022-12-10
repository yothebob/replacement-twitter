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
    post_creator_username = serializers.SerializerMethodField()
    account_post_color = serializers.SerializerMethodField()
    post_creator_post_color = serializers.SerializerMethodField()
    stripped_video = serializers.SerializerMethodField()
    stripped_image = serializers.SerializerMethodField()
    timeCreated = serializers.CharField(source="created")
    
    def get_account_username(self, obj):
        return obj.account.username
 
    def get_post_creator_username(self, obj):
        return obj.post_creator.username
 
    def get_stripped_video(self, obj):
        if str(obj.video) != "":
            return str(obj.video).replace(str(BASE_DIR), "")
        return ""

    def get_stripped_image(self, obj):
        if obj.image:
            return "/account-static/" + str(obj.image)
        return ""

    def get_account_post_color(self, obj):
        return obj.account.post_color

    def get_post_creator_post_color(self, obj):
        return obj.post_creator.post_color

    class Meta:
        model = Post
        fields = ['id', 'title', 'timeCreated', 'content', 'account', 'post_creator', "post_creator_username", "stripped_image", "stripped_video", 'account_username', 'account_post_color','post_creator_post_color' , 'blog', 'likes', "comments"]

        
# Serializers define the API representation.
class AccountSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    stripped_profile_photo = serializers.SerializerMethodField()
    stripped_background_photo = serializers.SerializerMethodField()
    
    def get_stripped_profile_photo(self, obj):
        if str(obj.profile_photo) != "":
            return "/account-static/" + str(obj.profile_photo)
        return ""
    
    def get_stripped_background_photo(self, obj):
        if str(obj.background_photo) != "":
            return "/account-static/" + str(obj.background_photo)
        return ""

    class Meta:
        model = Account
        fields = ["id",'username', 'name', "stripped_profile_photo","stripped_background_photo", 'following', "posts", "post_color"]


# a serializer to pass account for another accounts following list
class AccountFollowedSerializer(serializers.ModelSerializer):
    stripped_profile_photo = serializers.SerializerMethodField()
    
    def get_stripped_profile_photo(self, obj):
        if str(obj.profile_photo) != "":
            return str(obj.profile_photo).replace(str(BASE_DIR), "")
        return ""
    
    class Meta:
        model = Account
        fields = ["id",'username', 'name', "stripped_profile_photo"]        

        
# a serializer to get a profile followers in alittle more detail ( for follow page )
class AccountFollowingSerializer(serializers.ModelSerializer):
    stripped_profile_photo = serializers.SerializerMethodField()
    stripped_background_photo = serializers.SerializerMethodField()
    followers = AccountFollowedSerializer(many=True, read_only=True)
    
    
    def get_stripped_profile_photo(self, obj):
        if str(obj.profile_photo) != "":
            return "/account-static/" + str(obj.profile_photo)
        return ""
    
    def get_stripped_background_photo(self, obj):
        if str(obj.background_photo) != "":
            return "/account-static/" + str(obj.background_photo)
        return ""

    class Meta:
        model = Account
        fields = ["id",'username', 'name', "stripped_profile_photo","stripped_background_photo", 'followers', "post_color"]        


        
class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    timeCreated = serializers.CharField(source="created")
    class Meta:
        model = Attachment
        fields = ['url', "timeCreated", 'post', 'name', 'file_path']


# class userPostsSerializer(serializers.HyperlinkedModelSerializer):
    
    
#     class Meta:
#         model = Account
#         fields = [
            
#         ]
