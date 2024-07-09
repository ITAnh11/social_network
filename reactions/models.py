from django_mongoengine import fields, Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField
from userprofiles.models import UserBasicInfo
from django.utils import timezone

class Reactions(Document):
    id = fields.SequenceField(primary_key=True)
    user = EmbeddedDocumentField(UserBasicInfo)
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    type = fields.StringField() # like, love, haha, wow, sad, angry, care
    created_at = fields.DateTimeField(default=timezone.now)
    updated_at = fields.DateTimeField(default=timezone.now)
    
    meta = {
        'db': 'social_network',
        'collection': 'reactions',
        'indexes': [
            'to_posts_id',
            'to_comment_id',
            'user.id',
        ]
    }
    
    def setTypeReaction(self, type):
        self.update(__raw__={'$set': {'type': type}})
