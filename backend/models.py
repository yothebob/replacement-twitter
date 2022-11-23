from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=100, default="user")
    password = models.CharField(max_length=100, default="password")
    name = models.CharField(max_length=100, default="user")
    following = models.ManyToManyField("Account", blank=True, related_name="followers")
    total_posts = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=100, default="new Post")
    content = models.TextField(default="Write your content here (Hint: you can use markdown!)")
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    blog = models.BooleanField(default=False)
    likes = models.ManyToManyField("Account", blank=True, related_name="post_liked")
    
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
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=1500, blank=True, null=True)
    likes = models.ManyToManyField("Account", blank=True, related_name="comment_liked")
    

    
