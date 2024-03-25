from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt, datetime

# Create your views here.
class PostsView(APIView):
    def get(self, request):
        pass
    
    def post(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            return Response({'warning': 'Unauthorized'}, status=401)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']
        except jwt.ExpiredSignatureError:
            return Response({'warning': 'Token expired'}, status=401)
        
        print(request.data)
        
        return Response({'success': 'Post created!'})

