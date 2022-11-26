from django.db import models

color_choices = (
    ("white","white"),
    ("red","red"),
    ("blue","blue"),
    ("green","green"),
    ("purple","purple"),
    ("pink","pink"),
)


class Account(models.Model):
    username = models.CharField(max_length=100, default="user")
    password = models.CharField(max_length=100, default="password")
    name = models.CharField(max_length=100, default="user")
    following = models.ManyToManyField("Account", blank=True, related_name="followers")
    total_posts = models.IntegerField(default=0)
    post_color = models.CharField(max_length=75, default="white",choices=color_choices)
    
    def __str__(self):
        return self.username
    
class Post(models.Model):
    title = models.CharField(max_length=100, default="new Post")
    content = models.TextField(default="Write your content here (Hint: you can use markdown!)")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="posts")
    blog = models.BooleanField(default=False)
    likes = models.ManyToManyField("Account", blank=True, related_name="post_liked")
    image = models.FilePathField(max_length=250, path="/var/www/replacement-twitter/account-static", null=True, blank=True)
    video = models.FilePathField(max_length=250, path="/var/www/replacement-twitter/account-static", null=True, blank=True)
    
    def __str__(self):
        return self.title;
    
class Attachment(models.Model):
    name = models.CharField(max_length=100, default="new filename")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name
    

    
class Comment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.CharField(max_length=1500, blank=True, null=True)
    likes = models.ManyToManyField("Account", blank=True, related_name="comment_liked")
    

    
