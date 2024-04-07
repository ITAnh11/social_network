from django.shortcuts import render

from rest_framework.views import APIView

# Create your views here.
class GetCommentsForPost(APIView):
    def post(self, request):
        pass

class GetCommentsForComment(APIView):
    def post(self, request):
        pass

class CreateCommentForPost(APIView):
    def post(self, request):
        pass

class CreateCommentForComment(APIView):
    def post(self, request):
        pass