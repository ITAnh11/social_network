# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse


def navbar(request):
    return render(request, "navbar/navbar.html")