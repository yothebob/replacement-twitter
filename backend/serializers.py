from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .models import Account, Post, Attachment, Comment
from replacement_twitter.settings import ACCOUNT_STATIC_ROOT



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
        if str(obj.video):
            return ACCOUNT_STATIC_ROOT + str(obj.video)
        return ""

    def get_stripped_image(self, obj):
        if obj.image:
            return ACCOUNT_STATIC_ROOT + str(obj.image)
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
        if obj.profile_photo:
            return ACCOUNT_STATIC_ROOT + str(obj.profile_photo)
        return ""
    
    def get_stripped_background_photo(self, obj):
        if obj.background_photo:
            return ACCOUNT_STATIC_ROOT + str(obj.background_photo)
        return ""

    class Meta:
        model = Account
        fields = ["id",'username', 'name', "stripped_profile_photo","stripped_background_photo", 'following', "posts", "post_color"]


# a serializer to pass account for another accounts following list
class AccountFollowedSerializer(serializers.ModelSerializer):
    stripped_profile_photo = serializers.SerializerMethodField()
    
    def get_stripped_profile_photo(self, obj):
        if obj.profile_photo:
            return ACCOUNT_STATIC_ROOT + str(obj.profile_photo)
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
        if obj.profile_photo:
            return ACCOUNT_STATIC_ROOT + str(obj.profile_photo)
        return ""
    
    def get_stripped_background_photo(self, obj):
        if obj.background_photo:
            return ACCOUNT_STATIC_ROOT + str(obj.background_photo)
        return ""

    class Meta:
        model = Account
        fields = ["id",'username', 'name', "stripped_profile_photo","stripped_background_photo", 'followers', "post_color"]        


        
class ChatroomSerializer(serializers.HyperlinkedModelSerializer):
    timeCreated = serializers.CharField(source="created")
    chatroom_messages = MessageSerializer(many=True, read_only=True)
    chatroom_accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Attachment
        fields = ['timeCreated', 'post', 'name', 'chatroom_accounts', 'chatroom_messages']

        
class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    timeCreated = serializers.CharField(source="created")
    class Meta:
        model = Attachment
        fields = ['url', "timeCreated", 'post', 'name', 'file_path']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    timeCreated = serializers.CharField(source="created")
    # from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sent_messages")
    # to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="messages")
    likes = models.ManyToManyField("Account", blank=True, related_name="messages_liked")
    stripped_image = serializers.SerializerMethodField()
    stripped_video = serializers.SerializerMethodField()

    def get_stripped_image(self, obj):
        if obj.image:
            return ACCOUNT_STATIC_ROOT + str(obj.image)
        return ""

    def get_stripped_video(self, obj):
        if obj.video:
            return ACCOUNT_STATIC_ROOT + str(obj.video)
        return ""
    
    
    class Meta:
        model = Attachment
        fields = ["timeCreated", 'content', 'name', 'from_account', 'to_account', 'likes', "stripped_image", "stripped_video"]

