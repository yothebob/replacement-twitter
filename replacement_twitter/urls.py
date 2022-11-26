"""replacement_twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers
from backend.views import  AttachmentViewSet, PostViewSet, AccountViewSet, login_account, like_item, CommentViewSet, add_comment, follow_account, create_post, validate_login

router = routers.DefaultRouter()
router.register(r'Account', AccountViewSet)
router.register(r'Post', PostViewSet)
router.register(r'Comment', CommentViewSet)
router.register(r'Attachment', AttachmentViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/login/', login_account),
    path('api/like/', like_item),
    path('api/comment/', add_comment),
    path('api/follow/', follow_account),
    path('api/post/', create_post),
    path('api/validate/', validate_login),
]
    
