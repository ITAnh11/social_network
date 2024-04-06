from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt, datetime

from users.models import User

from .models import Posts, MediaOfPosts

from .serializers import PostsSerializer, MediaOfPostsSerializer

from common_functions.common_function import getUserProfileForPosts, getTimeDuration

# Create your views here.
def getUser(request):
    token = request.COOKIES.get('jwt')

    if not token:
        return None

    try:
        payload = jwt.decode(jwt=token, key='secret', algorithms=['HS256'])  
    except jwt.ExpiredSignatureError:
        return None
    
    return User.objects.filter(id=payload['id']).first()

class PostsPageView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return HttpResponseRedirect(reverse('users:login'))
        
        return render(request, 'posts/posts.html')
class CreatePostsView(APIView):
    
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        # print(request.data)
        # print(request.FILES)
        
        post = self.createPost(user, request)
        if type(post) != Posts:
            return post
        
        listMedia = self.createMediaOfPost(post, request.FILES.getlist('media'))
        if type(listMedia) != list:
            post.delete()
            return listMedia    
        
        data = []
        
               
        posts_data = PostsSerializer(post).data
        
        posts_data['media'] = MediaOfPostsSerializer(listMedia, many=True).data
        posts_data['user'] = getUserProfileForPosts(user)

        posts_data['created_at'] = getTimeDuration(post.created_at)
        
        data.append(posts_data)
        
        return Response({'success': 'Post created!',
                         'posts': data})

    def createPost(self, user, request):
        try:
            post = Posts.objects.create(
                user_id=user,
                title=request.data.get('title') or None,
                content=request.data.get('content') or None,
                status='public'
            )
            
            post.save()
        except:
            # print(1)
            return Response({'error': 'Error while saving post'}, status=400)
        
        return post
    
    def createMediaOfPost(self, post, media):
        
        # print('media:', media)
        try:
            listMediaOfPosts = []
            for file in media:
                if not file.content_type.startswith('image') and not file.content_type.startswith('video'):
                    # print('not image or video')
                    return Response({'error': 'File is not an image or video'}, status=400)
                
                mediaOfPosts = MediaOfPosts.objects.create(
                    post_id=post,
                    media=file
                )
                
                listMediaOfPosts.append(mediaOfPosts)
            
            for obj in listMediaOfPosts:
                # print('saving media')
                obj.save()
        except:
            # print('cant save media')
            return Response({'error': 'Error while saving media'}, status=400)
        
        return listMediaOfPosts
class CreatePostsAfterSetMediaProfileView():
    def createAvatarPosts(self, user, avatar):
        # print('avatar:', avatar)
        try:
            post = Posts.objects.create(
                user_id=user,
                title='Set avatar',
                content="Hello world",
                status='public'
            )
            
            ret = CreatePostsView().createMediaOfPost(post, [avatar])
            if ret != True:
                post.delete()
                return ret
            
            post.save()
        except:
            # print('cant save post')
            return Response({'error': 'Error while saving post'}, status=400)
    
    def createBackgroundPosts(self, user, background):
        # print('background:', background)
        try:
            post = Posts.objects.create(
                user_id=user,
                title='Set background',
                content=None,
                status='public'
            )
                        
            ret = CreatePostsView().createMediaOfPost(post, [background])
            if ret != True:
                post.delete()
                return ret
            
            post.save()
        except:
            # print('cant save post')
            return Response({'error': 'Error while saving post'}, status=400)
        