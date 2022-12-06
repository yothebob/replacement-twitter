from django.db import models

color_choices = (
    ("white","white"),
    ("red","red"),
    ("blue","blue"),
    ("green","green"),
    ("purple","purple"),
    ("pink","pink"),
)

# TODO: switch to attachment model
    
class Attachment(models.Model):
    name = models.CharField(max_length=100, default="new filename")
    file = models.FilePathField(max_length=500, path="/var/www/replacement-twitter/account-static", null=True, blank=True)
    is_image = models.BooleanField(default=None, null=True)
    is_video = models.BooleanField(default=None, null=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    username = models.CharField(max_length=100, default="user")
    password = models.CharField(max_length=100, default="password")
    name = models.CharField(max_length=100, default="user")
    following = models.ManyToManyField("Account", blank=True, related_name="followers")
    profile_photo = models.ForeignKey(Attachment, on_delete=models.CASCADE, default=None, null=True, related_name="account_profile_photo")
    # profile_photo = models.FilePathField(max_length=250, path="/var/www/replacement-twitter/account-static", null=True, blank=True)
    # background_photo = models.FilePathField(max_length=250, path="/var/www/replacement-twitter/account-static", null=True, blank=True)
    background_photo = models.ForeignKey(Attachment, on_delete=models.CASCADE, default=None, null=True, related_name="account_background_photo")
    total_posts = models.IntegerField(default=0)
    post_color = models.CharField(max_length=75, default="white",choices=color_choices)
    
    def __str__(self):
        return self.username

    
class Post(models.Model):
    title = models.CharField(max_length=100, default="new Post")
    content = models.TextField(default="Write your content here (Hint: you can use markdown!)")
    post_creator = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=True, related_name="created_post")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="posts")
    blog = models.BooleanField(default=False)
    likes = models.ManyToManyField("Account", blank=True, related_name="post_liked")
    # image = models.FilePathField(max_length=250, path="/var/www/replacement-twitter/account-static", null=True, blank=True)
    image = models.ForeignKey(Attachment, on_delete=models.CASCADE, default=None, null=True, related_name="post_image")
    video = models.FilePathField(max_length=250, path="/var/www/replacement-twitter/account-static", null=True, blank=True)
    
    def __str__(self):
        return self.title;
    

class Message(models.Model):
    content = models.TextField(default="")
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sent_messages")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="messages")
    likes = models.ManyToManyField("Account", blank=True, related_name="messages_liked")
    image = models.ForeignKey(Attachment, on_delete=models.CASCADE, default=None, null=True, related_name="message_image")

    def __str__(self):
        return self.content;

    
    
class Comment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.CharField(max_length=1500, blank=True, null=True)
    likes = models.ManyToManyField("Account", blank=True, related_name="comment_liked")
    

    
