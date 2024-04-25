from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Posts, MediaOfPosts, PostsInfo

from .serializers import PostsSerializer, MediaOfPostsSerializer, PostsInfoSerializer

from common_functions.common_function import getUserProfileForPosts, getTimeDuration, getUser

# Create your views here.
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
        
        listMedia = self.createMediaOfPosts(post, request.FILES.getlist('media'))
        if type(listMedia) != list:
            post.delete()
            return listMedia    
        
        if len(listMedia) == 0 and not post.content:
            return Response({'error': 'No posts uploaded'}, status=400)
        
        postsInfo = PostsInfo()
        postsInfo.setPostsId(post.id)
        postsInfo.save()
        
        data = []
        
        posts_data = PostsSerializer(post).data
        
        posts_data['media'] = MediaOfPostsSerializer(listMedia, many=True).data
        posts_data['user'] = getUserProfileForPosts(user)
        posts_data['posts_info'] = PostsInfoSerializer(postsInfo).data

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
    
    def createMediaOfPosts(self, post, media):
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
        except Exception as e:
            # print('cant save media')
            print('createMediaOfPosts', e)
            return Response({'error': 'Error while saving media'}, status=400)
        
        return listMediaOfPosts
    
class CreatePostsAfterSetImageProfileView():
    def createUpdateImageProfilePosts(self, user, typeImage, image):
        
        # print('createUpdateImageProfilePosts', user, typeImage, image)
        try:
            post = Posts.objects.create(
                user_id=user,
                title=f"updated {typeImage} profile picture ",
                content='',
                status='public'
            )
            
            postsInfo = PostsInfo()
            postsInfo.setPostsId(post.id)
            
            mediaOfPosts = self.createMediaOfPosts(post, image)
            if type(mediaOfPosts) != MediaOfPosts:
                post.delete()
                return mediaOfPosts
            
            postsInfo.save()
            post.save()
            
        except Exception as e:
            print('createUpdateImageProfilePosts', e)
            return Response({'error': 'Error while saving post'}, status=400)
        
        return post
    
    def createMediaOfPosts(self, post, media):
        try:
            mediaOfPosts = MediaOfPosts.objects.create(
                post_id=post,
                media=media
            )
            
            mediaOfPosts.save()
        except Exception as e:
            print('createMediaOfPosts', e)
            return Response({'error': 'Error while saving media'}, status=400)
        
        return mediaOfPosts
    
class GetPostsPageView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        params = request.GET
        if not params.get('id'):
            return Response({'error': 'No id provided'}, status=400)
        
        idPostsRequest = int(params.get('id'))
        
        try:
            posts = Posts.objects.filter(id=idPostsRequest).first()
            
            # print(str(Posts.objects.filter(id=idPostsRequest).query.explain(using='default')))
            
        except Posts.DoesNotExist:
            return Response({'error': 'No posts found'}, status=404)
        
        mediaOfPosts = MediaOfPosts.objects.filter(post_id=posts)
        
        # print(str(MediaOfPosts.objects.filter(post_id=posts).query.explain(using='default')))
        
        postsSerializer = PostsSerializer(posts)
        mediaOfPostsSerializer = MediaOfPostsSerializer(mediaOfPosts, many=True)
        
        postsData = postsSerializer.data
        postsData['media'] = mediaOfPostsSerializer.data
        postsData['created_at'] = getTimeDuration(posts.created_at)
        postsData['posts_info'] = self.getPostsInfo(posts)
        
        context = {
            'posts': postsData
        }
        
        print(postsData)
        
        return render(request, 'posts/posts_page.html', context=context)
    
    def getPostsInfo(self, posts):
        try:
            postsInfo = PostsInfo.objects(__raw__={'posts_id': posts.id}).first()
        except PostsInfo.DoesNotExist:
            return Response({'error': 'No posts info found'}, status=404)
        
        return PostsInfoSerializer(postsInfo).data
    