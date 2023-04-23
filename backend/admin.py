from django.contrib import admin
from backend.models import *

admin.site.register(Post)
admin.site.register(Account)
admin.site.register(Attachment)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Chatroom)
admin.site.register(Notification)

# Register your models here.
