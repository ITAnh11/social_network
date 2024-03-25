from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView

import jwt

from users.models import User
from users.serializers import UserSerializer

class ProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return HttpResponseRedirect(reverse('users:login'))

        try:
            payload = jwt.decode(jwt=token, key='secret', algorithms=['HS256'])  
        except jwt.ExpiredSignatureError:
            return HttpResponseRedirect(reverse('users:login'))

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)

        return render(request, 'userprofiles/profile_demo.html', {"user": serializer.data})
