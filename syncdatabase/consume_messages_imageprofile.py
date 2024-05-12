import os
import sys
from pathlib import Path

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

# Add the parent directory of the current script to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import django
django.setup()

from django.core.files.storage import default_storage
from confluent_kafka import Consumer
from posts.models import Posts
from reactions.models import Reactions
from comments.models import Comments
from notifications.models import Notifications
from userprofiles.views import UserProfileBasicView
import json
import logging
logger = logging.getLogger(__name__)

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=2)

def update_data(model, query, update):
    try:
        model.objects(__raw__=query).update(__raw__=update)
    except Exception as e:
        logger.error('Error update data:', e)

# This function processes a Kafka message and updates the database accordingly.
def process_message_imageprofile(msg):
    # This function processes a Kafka message and updates the database accordingly.
    # You'll need to replace this with your own logic.
    # Decode the Kafka message
    if msg.value() is None:
        print('No message')
        return
    
    logger.info('Begin process message Imageprofile')
    
    try:
        msg_value = msg.value().decode('utf-8')

        # Parse the message as JSON
        msg_json = json.loads(msg_value)

        # Get the operation type
        op = msg_json['payload']['op']

        # Get the after data
        after_data = msg_json['payload']['after']

        # Perform the appropriate action in MongoDB based on the operation type
        if op == 'u':
            print("process_message_update_avatar", msg_json)
            logger.info("process_message_update_avatar", msg_json)
            
            # Get the user ID
            user_id = after_data['user_id_id']
            
            new_avatar = after_data['avatar']
            
            new_avatar_path = default_storage.url(new_avatar)
            
            # Delete all post from the database
            executor.submit(update_data, Posts, {'user.id': user_id}, {'$set': {'user.avatar': new_avatar_path}})
            
            # Delete all reaction from the database
            executor.submit(update_data, Reactions, {'user.id': user_id}, {'$set': {'user.avatar': new_avatar_path}})
            
            # Delete all comment from the database
            executor.submit(update_data, Comments, {'user.id': user_id}, {'$set': {'user.avatar': new_avatar_path}})
            
            # Delete all notification from the database
            executor.submit(update_data, Notifications, {'to_user_id': user_id}, {'$set': {'user.avatar': new_avatar_path}})
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Process message Imageprofile error:', e)
        logger.error('Process message Imageprofile error:', e)
        
    print('Processed message Imageprofile done!!!')
    logger.info('End process message Imageprofile')

def consume_messages_imageprofile():
    print('Consuming messages imageprofile')
    logger.info('Consuming messages imageprofile')
    # Create a Kafka consumer
    c = Consumer({
        'bootstrap.servers': 'localhost:29092',
        'group.id': 'my_group',
        'auto.offset.reset': 'earliest'
    })

    # Subscribe to the Kafka topic
    c.subscribe(['social_network.public.userprofiles_imageprofile'])

    try:
        while True:
            # Poll for messages from Kafka
            msg = c.poll(1.0)
            if msg is None:
                continue
            elif msg.error():
                print("Consumer error: {}".format(msg.error()))
                logger.error("Consumer error: {}".format(msg.error()))
                continue
            else:
                # Process the Kafka message
                process_message_imageprofile(msg)
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown(wait=True)
        c.close()