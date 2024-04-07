from django.utils import timezone
from datetime import timedelta


from userprofiles.models import UserProfile, ImageProfile
from userprofiles.serializers import UserProfileSerializer, ImageProfileSerializer
from users.models import User

import jwt

def getUserProfileForPosts(user):
        userprofile = UserProfile.objects.filter(user_id=user).values('first_name', 'last_name').first()
        imageprofile = ImageProfileSerializer(ImageProfile.objects.filter(user_id=user).values('avatar').first())
        
        data = {
            "id": user.id,
            "name": f"{userprofile.get('first_name')} {userprofile.get('last_name')}",
            "avatar": imageprofile.data.get('avatar')
        }
        
        return data

def getTimeDuration(created_at):
        time_duration = timezone.now() - created_at
        if time_duration < timedelta(minutes=1):
            return f'{time_duration.seconds} seconds ago'
        elif time_duration < timedelta(hours=1):
            return f'{time_duration.seconds//60} minutes ago'
        elif time_duration < timedelta(days=1):
            return f'{time_duration.seconds//3600} hours ago'
        else:
            return f'{time_duration.days} days ago'

def getUser(request):
    token = request.COOKIES.get('jwt')
    
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
    except jwt.ExpiredSignatureError:
        return None
    
    user = User.objects.get(id=user_id)
    
    return user