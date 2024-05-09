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
import logging
logger = logging.getLogger(__name__)
# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=2)

def delete_data(model, query):
    try:
        model.objects(__raw__=query).delete()
    except Exception as e:
        logger.error('Error delete data:', e)
        # print('Error delete data:', e)
    
def delete_all_posts(user_id):
    try:
        posts = Posts.objects(__raw__={'user.id': user_id})
        for post in posts:
            # print('Delete post:', post.id)
            
            medias = MediaOfPosts.objects(__raw__={'post_id': post.id})
            for media in medias:
                try:
                    logger.info('Delete media:', media.id)
                    media.delete_media()
                except Exception as e:
                    logger.error('Error delete media:', e)
                    print('Error delete media:', e)
        
        for post in posts:
            try:
                logger.info('Delete post:', post.id)
                post.delete()
            except Exception as e:
                logger.error('Error delete post:', e)
                print('Error delete post:', e)

    except Exception as e:
        logger.error('Error delete all posts:', e)
        print('Error delete all posts:', e)
        

# This function processes a Kafka message and updates the database accordingly.
def process_message_user(msg):
    # This function processes a Kafka message and updates the database accordingly.
    # You'll need to replace this with your own logic.
    # Decode the Kafka message
    if msg.value() is None:
        print('No message')
        return
    logger.info('Begin process message User')
    try:
        msg_value = msg.value().decode('utf-8')

        # Parse the message as JSON
        msg_json = json.loads(msg_value)

        # Get the operation type
        op = msg_json['payload']['op']

        # Get the before data
        before_data = msg_json['payload']['before']
        
        # Perform the appropriate action in MongoDB based on the operation type
        if op == 'd':
            
            print("process_message_delete_user", msg_json)
            logger.info("process_message_delete_user", msg_json)
            
            # Get the user ID
            user_id = before_data['id']
            
            executor.submit(UserProfileBasicView().removeUserProfileBasic, user_id)
            executor.submit(delete_all_posts, user_id)
            executor.submit(delete_data, Reactions, {'user.id': user_id})
            executor.submit(delete_data, Comments, {'user.id': user_id})
            executor.submit(delete_data, Notifications, {'to_user_id': user_id})

        print('Processed message User done!!!')
        logger.info('Processed message User done!!!')
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error('Error processing message User:', e)
        # print('Error processing message User:', e)
        
    
def consume_messages_user():
    logger.info("Consuming messages user")
    print("Consuming messages user")
    # Create a Kafka consumer
    c = Consumer({
        'bootstrap.servers': 'localhost:29092',
        'group.id': 'my_group',
        'auto.offset.reset': 'earliest'
    })

    # Subscribe to the Kafka topic
    c.subscribe(['social_network.public.users_user'])
    
    try:
        while True:
            # Poll for messages from Kafka
            msg = c.poll(1.0)
            if msg is None:
                continue
            elif msg.error():
                # print("Consumer error: {}".format(msg.error()))
                logger.error("Consumer error: {}".format(msg.error()))
                continue
            else:
                # Process the Kafka message
                process_message_user(msg)
    except KeyboardInterrupt:
        pass
    finally:
        c.close()
        executor.shutdown(wait=True)