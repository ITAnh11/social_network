from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Posts, MediaOfPosts
from userprofiles.views import UserProfileBasicView

from .serializers import PostsSerializer, MediaOfPostsSerializer

from common_functions.common_function import getTimeDuration, getUser

from django.core.cache import caches

import json

redis_server = caches['redis']

import logging 
logger = logging.getLogger(__name__)
def createMediaOfPosts(post, medias):
    listMediaOfPosts = []
    try:
        for media in medias:
            mediaOfPosts = MediaOfPosts(
                post_id=post.id
            )
            
            mediaOfPosts.save_media(media)
            
            listMediaOfPosts.append(mediaOfPosts)
    except Exception as e:
        logger.error('createMediaOfPosts: %s', e)
        print('createMediaOfPosts', e)
        return False

    for mediaOfPosts in listMediaOfPosts:
        try:
            mediaOfPosts.save()
        except Exception as e:
            logger.error('createMediaOfPosts: %s', e)
            print('saveMediaOfPosts', e)
            return False

    return listMediaOfPosts

# Create your views here.
class CreatePostsView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            logger.warning("User is not authenticated.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        userProfileBasic = UserProfileBasicView().getUserProfileBasic(user)
        
        post = self.createPosts(userProfileBasic, 
                                request.data.get('title'), 
                                request.data.get('content'), 
                                request.data.get('status'))
        
        if post == False:
            logger.error("Error while creating post.")
            return Response({'error': 'Error while creating post'}, status=400)
        
        # print('request.data', request.data)

        logger.info('Post created successfully.')
        logger.debug('Request data: %s', request.data)

        medias = request.FILES.getlist('media')
        
        # print('medias', medias)
        logger.debug('Medias: %s', medias)
        listMediaOfPost = createMediaOfPosts(post, medias)
        
        if listMediaOfPost == False:
            for mediaOfPost in listMediaOfPost:
                mediaOfPost.delete()
            post.delete()
            logger.error("Error while saving media.")
            return Response({'error': 'Error while saving media'}, status=400)
        
        post_data = PostsSerializer(post).data
        post_data['media'] = MediaOfPostsSerializer(listMediaOfPost, many=True).data
        post_data['created_at'] = getTimeDuration(post.created_at)
        
        data = []
        data.append(post_data)
        
        return Response({'success': 'Post created!',
                         'posts': data})
        
    def createPosts(self, user, title, content, status):
        try:
            post = Posts.objects.create(
                user=user,
                title=title,
                content=content,
                status=status,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            post.save()
        except Exception as e:
            logger.error('createPosts: %s', e)
            print('createPosts', e)
            return False
                
        return post
        
def createUpdateImageProfilePosts(userprofilebasic, typeImage, image):
    try:
        post = Posts.objects.create(
                            user=userprofilebasic,
                            title=f"updated {typeImage} profile picture",
                            content='',
                            status='public',
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
        
        listMediaOfPost = createMediaOfPosts(post, [image])
        
        if listMediaOfPost == False:
            for mediaOfPost in listMediaOfPost:
                mediaOfPost.delete()
            post.delete()
            logger.error("Error while saving media.")
            return False
        
        post.save()
        
    except Exception as e:
        logger.error('createUpdateImageProfilePosts: %s', e)
        print('createUpdateImageProfilePosts', e)
        return False
    
    return post
     
class GetPostsPageView(APIView):
    def get(self, request):
        try:
            user = getUser(request)
        except Exception as e:
            return HttpResponseRedirect(reverse('users:login'))
        
        if not user:
            logger.warning("User is not authenticated.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        params = request.GET
        posts_id = params.get('posts_id')
        image_id = params.get('image_id')
        
        if not posts_id or not image_id:
            logger.error("Invalid request.")
            return Response({'error': 'Invalid request'}, status=400)
        
        idPostsRequest = int(posts_id)
        idImageRequest = int(image_id)
        
        post = Posts.objects(__raw__={'_id': idPostsRequest}).first()
        
        if not post:
            logger.error("Post not found.")
            print('Post not found')
            return Response({'error': 'Post not found'}, status=404)
        
        mediaOfPosts = MediaOfPosts.objects(__raw__={'post_id': idPostsRequest}).all()
        
        # print(str(MediaOfPosts.objects.filter(post_id=posts).query.explain(using='default')))
        
        postsSerializer = PostsSerializer(post)
        mediaOfPostsSerializer = MediaOfPostsSerializer(mediaOfPosts, many=True)
        
        postsData = postsSerializer.data
        postsData['media'] = mediaOfPostsSerializer.data
        postsData['created_at'] = getTimeDuration(post.created_at)
                
        context = {
            'post': postsData,
            'image_id': idImageRequest,
        }
        
        return render(request, 'posts/posts_page.html', context=context)
class GetPostsForProfilePageView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            logger.warning("User is not authenticated.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        
        if request.query_params.get('id'):
            idUserRequested = int(request.query_params.get('id'))
        else:  
            idUserRequested = user.id
        
        num_posts = Posts.objects(__raw__={'user.id': idUserRequested}).count()
        currentNumberOfPosts = int(request.data.get('current_number_of_posts'))

        if currentNumberOfPosts >= num_posts:
            logger.error("No more posts available.")
            return Response({'error': 'No more posts available'}, status=400)

        posts = Posts.objects(__raw__={'user.id': idUserRequested}).order_by('-created_at')[currentNumberOfPosts:currentNumberOfPosts+10]
        
        for post in posts:
            posts_data = PostsSerializer(post).data
            media_of_posts = MediaOfPosts.objects(__raw__={'post_id': post.id}).all()
            media_data = MediaOfPostsSerializer(media_of_posts, many=True).data
            
            posts_data['media'] = media_data

            posts_data['created_at'] = getTimeDuration(post.created_at)
        
            data.append(posts_data)
            
        reponse = Response()
        
        reponse.data = {
            'posts': data,
            'isOwner': True if user.id == idUserRequested else False
        }

        return reponse

class GetPostsForHomePageView(APIView):
    def post(self, request):
        pass
        user = getUser(request)
        
        if not user:
            logger.warning("User is not authenticated.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        reponse = Response()
        
        data = []

        posts = self.filterPosts(user.id)

        try: 
            for post in posts:
                
                posts_data = PostsSerializer(post).data
                
                media = MediaOfPosts.objects(__raw__={'post_id': post.id}).all()
                media_data = MediaOfPostsSerializer(media, many=True).data
                
                posts_data['media'] = media_data
                posts_data['created_at'] = getTimeDuration(post.created_at)
            
                data.append(posts_data)
        except Exception as e:
            logger.error(e)
            print(e)
            
        reponse.data = {
            'posts': data
        }

        return reponse
    
    def filterPosts(self, user_id):
        try:        
            # Get all posts that the user has not watched
            
            watched_posts = redis_server.get(f'user:{user_id}:watched_posts')

            # Kiểm tra nếu dữ liệu không phải là None
            if watched_posts:
                # Nếu dữ liệu là chuỗi JSON, chuyển đổi nó thành danh sách
                if isinstance(watched_posts, str):
                    watched_posts = json.loads(watched_posts)
                
                # Chuyển đổi các phần tử trong danh sách thành số nguyên
                posts_is_watched_ids = [int(id) for id in watched_posts]
            else:
                posts_is_watched_ids = []
            logger.debug('posts_is_watched_ids: %s', posts_is_watched_ids)
            print('posts_is_watched_ids', posts_is_watched_ids)

            posts_not_watched = Posts.objects(__raw__={'user.id': {'$ne': user_id}, 
                                                       '_id': {'$nin': posts_is_watched_ids}}).order_by('-created_at')[:10]
            
        except Exception as e:
            logger.error(e)
            return []
        return posts_not_watched
    
class MarkPostAsWatchedView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            logger.warning("User is not authenticated.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = request.data
        post_ids = data.getlist('post_ids[]')
        
        post_ids = set(post_ids)
        post_ids = list(post_ids)
        
        for post_id in post_ids:
        
            if not post_id:
                continue
            
            idPostsRequest = int(post_id)
            
            try:
                post = Posts.objects(__raw__={'_id': idPostsRequest}).first()
            except Posts.DoesNotExist:
                continue
            
            # Lấy danh sách hiện tại từ Redis
            watched_posts = redis_server.get(f'user:{user.id}:watched_posts')

            # Nếu danh sách hiện tại là None, khởi tạo danh sách rỗng
            if watched_posts is None:
                watched_posts = []

            # Nếu danh sách hiện tại là chuỗi JSON, chuyển đổi nó thành danh sách
            if isinstance(watched_posts, str):
                watched_posts = json.loads(watched_posts)

            # Thêm ID mới vào danh sách
            watched_posts.append(post.id)
            
            # Lưu lại danh sách đã cập nhật vào Redis
            redis_server.set(f'user:{user.id}:watched_posts', json.dumps(watched_posts))

            # Kiểm tra TTL của khóa
            ttl = redis_server.ttl(f'user:{user.id}:watched_posts')

            # Nếu TTL là -1 (không có TTL), thiết lập TTL cho khóa
            if ttl == -1:
                redis_server.expire(f'user:{user.id}:watched_posts', 3600 * 24)  # 24 giờ
                    
        return Response({'success': 'Post is marked as watched!'})