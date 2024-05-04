# chat/views.py
from django.shortcuts import render
import logging
logger=logging.getLogger(__name__)

def index(request):
    logger.info('access to mess')
    return render(request, "mess/index.html")

def room(request, room_name):
    logger.info('access to room_mess')
    return render(request, "mess/room.html", {"room_name": room_name})