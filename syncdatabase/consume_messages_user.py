import os
import sys
from pathlib import Path

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

# Add the parent directory of the current script to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import django
django.setup()

from confluent_kafka import Consumer
import json
from concurrent.futures import ThreadPoolExecutor

from posts.models import Posts
from reactions.models import Reactions
from comments.models import Comments
from notifications.models import Notifications
from posts.models import MediaOfPosts
from userprofiles.views import UserProfileBasicView

# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=2)

def delete_data(model, query):
    model.objects(__raw__=query).delete()
    
def delete_all_posts(user_id):
    try:
        posts = Posts.objects(__raw__={'user.id': user_id})
        for post in posts:
            print('Delete post:', post.id)
            medias = MediaOfPosts.objects(__raw__={'post_id': post.id})
            for media in medias:
                media.delete_media()
        
        for post in posts:
            post.delete()
    except Exception as e:
        print('Error delete all posts:', e)
        

# This function processes a Kafka message and updates the database accordingly.
def process_message_user(msg):
    # This function processes a Kafka message and updates the database accordingly.
    # You'll need to replace this with your own logic.
    # Decode the Kafka message
    if msg.value() is None:
        print('No message')
        return
    
    try:
        msg_value = msg.value().decode('utf-8')

        # Parse the message as JSON
        msg_json = json.loads(msg_value)

        # Get the operation type
        op = msg_json['payload']['op']

        # Get the before data
        before_data = msg_json['payload']['before']
        # Get the after data
        after_data = msg_json['payload']['after']

        # Perform the appropriate action in MongoDB based on the operation type
        if op == 'd':
            
            # print("process_message_delete_user", msg_json)
            
            # Get the user ID
            user_id = before_data['id']
            
            executor.submit(UserProfileBasicView().removeUserProfileBasic, user_id)
            executor.submit(delete_all_posts, user_id)
            executor.submit(delete_data, Reactions, {'user.id': user_id})
            executor.submit(delete_data, Comments, {'user.id': user_id})
            executor.submit(delete_data, Notifications, {'to_user_id': user_id})

        print('Processed message User done!!!')
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Error processing message User:', e)
        
    
def consume_messages_user():
    # Create a Kafka consumer
    c = Consumer({
        'bootstrap.servers': 'localhost:29092',
        'group.id': 'my_group',
        'auto.offset.reset': 'earliest'
    })

    # Subscribe to the Kafka topic
    c.subscribe(['social_network.public.users_user'])

    while True:
        # Poll for messages from Kafka
        msg = c.poll(1.0)
        if msg is None:
            continue
        elif msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        else:
            # Process the Kafka message
            process_message_user(msg)

    c.close()