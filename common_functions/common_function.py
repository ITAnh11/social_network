from django.utils import timezone
from datetime import timedelta


from userprofiles.models import UserProfile, ImageProfile
from userprofiles.serializers import ImageProfileSerializer
from users.models import User

import jwt

def getUserProfileForPosts(user):
        userprofile = UserProfile.objects.filter(user_id=user).values('first_name', 'last_name').first()
        imageprofile = ImageProfileSerializer(ImageProfile.objects.filter(user_id=user).first())
                
        data = {
            "id": user.id,
            "name": f"{userprofile.get('first_name')} {userprofile.get('last_name')}",
            "avatar": imageprofile.data.get('avatar')
        }
        
        return data

def getTimeDuration(created_at):
    created_at = created_at.replace(tzinfo=timezone.utc)
    time_duration = timezone.now() - created_at
    if time_duration < timedelta(minutes=1):
        return f'{time_duration.seconds} seconds ago'
    elif time_duration < timedelta(hours=1):
        return f'{time_duration.seconds//60} minutes ago'
    elif time_duration < timedelta(days=1):
        return f'{time_duration.seconds//3600} hours ago'
    elif time_duration < timedelta(days=7):
        return f'{time_duration.days} days ago'
    return created_at.strftime('%d, %B %Y')

def getTimeDurationForComment(created_at):
    created_at = created_at.replace(tzinfo=timezone.utc)
    time_duration = timezone.now() - created_at
    if time_duration < timedelta(minutes=1):
        return f'{time_duration.seconds} s'
    elif time_duration < timedelta(hours=1):
        return f'{time_duration.seconds//60} m'
    elif time_duration < timedelta(days=1):
        return f'{time_duration.seconds//3600} h'
    elif time_duration < timedelta(days=7):
        return f'{time_duration.days} d'
    elif time_duration < timedelta(days=30):
        return f'{time_duration.days//7} w'
    elif time_duration < timedelta(days=365):
        return f'{time_duration.days//30} m'
    return f'{time_duration.days//365} y'

def getUser(request):
    token = request.COOKIES.get('jwt')
    
    if not token:
        return {'error': 'Unauthorized'}
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
    except jwt.ExpiredSignatureError:
        return {'error': 'Unauthorized'}
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Exception('User not found')
    
    return user

def getAllUsers():
     return User.objects.filter()