from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .models import Account, Post, Attachment, Comment, Message, Chatroom, Notification
from replacement_twitter.settings import ACCOUNT_STATIC_ROOT
import pytz


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
    notification_id = serializers.SerializerMethodField()
    
    def get_stripped_profile_photo(self, obj):
        if obj.profile_photo:
            return ACCOUNT_STATIC_ROOT + str(obj.profile_photo)
        return ""
    
    def get_notification_id(self, obj):
        last_not = Notification.objects.filter(To=obj).last()
        if last_not is not None:
            return last_not.id
        else:
            return 0
    
    def get_stripped_background_photo(self, obj):
        if obj.background_photo:
            return ACCOUNT_STATIC_ROOT + str(obj.background_photo)
        return ""

    class Meta:
        model = Account
        fields = ["id",'username', 'name', "stripped_profile_photo","stripped_background_photo", 'following', "posts", "post_color", "notification_id"]

# slimmer accountSerializer AKA no posts
class FKAccountSerializer(serializers.ModelSerializer):
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
        fields = ["id",'username', 'name', "stripped_profile_photo","stripped_background_photo", 'following', "post_color"]


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

        
class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    timeCreated = serializers.CharField(source="created")
    videoType = serializers.SerializerMethodField()

    def get_videoType(self, obj):
        return f"video/{obj.ext}"
    
    class Meta:
        model = Attachment
        fields = ["id", 'url', "timeCreated", 'videoType', 'name']

        
class MessageSerializer(serializers.HyperlinkedModelSerializer):
    timeCreated = serializers.DateTimeField(source="created", format="%b %d %I:%M:%S", default_timezone=pytz.timezone("US/Pacific"))
    from_account = FKAccountSerializer(read_only=True)
    chatroom = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all())
    messages_liked = FKAccountSerializer(many=True, read_only=True)
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
        model = Message
        fields = ["id", "timeCreated", 'content', 'from_account', 'chatroom', 'messages_liked', "stripped_image", "stripped_video"]

        
class ChatroomSerializer(serializers.HyperlinkedModelSerializer):
    timeCreated = serializers.CharField(source="created")
    chatroom_messages = serializers.SerializerMethodField()
    chatroom_accounts = FKAccountSerializer(many=True, read_only=True)

    def get_chatroom_messages(self, obj):
        query = Message.objects.filter(chatroom=obj).order_by('-id')[:30]
        serializer = MessageSerializer(query ,many=True)
        return serializer.data

    class Meta:
        model = Chatroom
        fields = ["id", 'timeCreated', 'name', 'chatroom_accounts', 'chatroom_messages']

class NotificationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Notification
        fields = ["id", 'notification_id', 'message']
