from django_mongoengine import fields, Document
from mongoengine.fields import EmbeddedDocumentField
from userprofiles.models import UserBasicInfo

class Notifications(Document):
    id = fields.SequenceField(primary_key=True)
    type = fields.StringField()
    user = EmbeddedDocumentField(UserBasicInfo)
    content = fields.StringField()
    to_user_id = fields.IntField()
    created_at = fields.DateTimeField()   
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
    
    meta = {
        'db': 'social_network',
        'collection': 'notifications',
        'indexes': [
            'to_user_id',
            'type',
        ],
        'allow_inheritance': True
    }

class ReactNotifitions(Notifications):
    type_reaction = fields.StringField()
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)

class CommentNotifications(Notifications):
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)

class AddFriendNotifications(Notifications):
    id_friend_request = fields.IntField()
    status_request = fields.StringField(default='pending')
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        
    def setAccept(self):
        self.update(__raw__={'$set': {'status_request': 'accepted'}})
    
    def setDecline(self):
        self.update(__raw__={'$set': {'status_request': 'declined'}})
