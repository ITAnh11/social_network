from django_mongoengine import fields, Document
from mongoengine.fields import EmbeddedDocumentField
from userprofiles.models import UserBasicInfo

class ReactNotifitions(Document):
    id = fields.SequenceField(primary_key=True)
    type = fields.StringField()
    user = EmbeddedDocumentField(UserBasicInfo)
    content = fields.StringField()
    type_reaction = fields.StringField()
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    to_user_id = fields.IntField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()    
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
    
    meta = {
        'db': 'social_network',
        'collection': 'notifications',
        'indexes': [
            'to_user_id',
            'type'
        ]
    }

class CommentNotifications(Document):
    id = fields.SequenceField(primary_key=True)
    type = fields.StringField()
    user = EmbeddedDocumentField(UserBasicInfo)
    content = fields.StringField()
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    to_user_id = fields.IntField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()    
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
    
    meta = {
        'db': 'social_network',
        'collection': 'notifications',
        'indexes': [
            'to_user_id',
            'type'
        ]
    }

class AddFriendNotifications(Document):
    id = fields.SequenceField(primary_key=True)
    type = fields.StringField()
    user = EmbeddedDocumentField(UserBasicInfo)
    content = fields.StringField()
    to_user_id = fields.IntField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()    
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
    
    meta = {
        'db': 'social_network',
        'collection': 'notifications',
        'indexes': [
            'to_user_id',
            'type'
        ]
    }